import { postgres as prisma, mongo } from "../config/db.js";
import { LearningPathService } from "./learningPath.service.js";

export class MLService {
  private static FASTAPI_URL =
    process.env.FASTAPI_URL || "http://127.0.0.1:8000";

  /**
   * Predict career recommendation for a user based on their profile, interests, and skills.
   */
  static async predictCareer(userId: string) {
    try {
      // 1. Fetch Comprehensive Learner Data from Postgres
      const profile = await prisma.learnerProfile.findUnique({
        where: { userId },
        include: {
          user: {
            include: {
              profile: true, // This is the UserProfile model in 'core' schema
            },
          },
          interests: {
            include: {
              interest: true,
            },
          },
          skills: {
            include: {
              skill: true,
            },
          },
        },
      });

      if (!profile) {
        throw new Error("Learner profile not found for the user.");
      }

      // 2. Extract and Format Features
      const rawGender = profile.user.profile?.gender || "Male";
      const gender =
        rawGender.charAt(0).toUpperCase() + rawGender.slice(1).toLowerCase();

      const interestNames = profile.interests
        .map((i) => i.interest?.name)
        .filter(Boolean)
        .join(", ");
      const skillNames = profile.skills
        .map((s) => s.skill?.name)
        .filter(Boolean)
        .join(", ");

      // Determine grades/CGPA mapping based on age group
      let grades = profile.cgpaPercentage;

      // Handle SECONDARY (SCHOOL) learners (13-18)
      // If grades are missing or format is different, use appropriate proxy/fallback
      if (profile.ageGroup === "SCHOOL" || profile.ageGroup === "CHILD") {
        // For school students, if grades are not explicitly set, we might use a default median
        // Or if they provided a 'grade' (e.g., 10th), we can infer a base score
        grades = grades || 80.0; // Higher baseline for school performance in this model
      } else {
        // College/Graduate/Professional
        grades = grades || 70.0; // Standard fallback
      }

      // 3. Call FastAPI Prediction Service
      const response = await fetch(
        `${this.FASTAPI_URL}/api/v1/career/predict`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            gender: gender,
            interest: interestNames || "Technology",
            skills: skillNames || "Communication",
            grades: grades,
          }),
        },
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`FastAPI Request Failed: ${errorText}`);
      }

      const prediction: any = await response.json();

      let predictionId = "temp-mongo-id-" + Date.now();
      try {
        // 4. Record Prediction in MongoDB (Non-Relational Storage)
        const mlPrediction = await mongo.mLPrediction.create({
          data: {
            userId: userId,
            inputFeatures: {
              gender,
              interests: interestNames,
              skills: skillNames,
              grades: grades,
            },
            predictedCourse: prediction.predicted_course,
            confidence: prediction.confidence.toString(),
            confidenceScore: prediction.confidence,
            alternativeCareers: prediction.top_predictions.map(
              (p: any) => p.course,
            ),
            alternativeScores: prediction.top_predictions.map(
              (p: any) => p.probability,
            ),
            modelVersion: "v1.0.0",
            modelType: "RandomForest",
          },
        });
        predictionId = mlPrediction.id;

        // 5. Create Career Recommendation Record
        await mongo.careerRecommendation.create({
          data: {
            userId: userId,
            predictionId: mlPrediction.id,
            careerTitle: prediction.predicted_course,
            careerDescription: `Based on your profile, the AI recommends a career in ${prediction.predicted_course}.`,
            requiredSkills: profile.skills.map((s) => s.skill.name),
            industryDemand: "High", // Placeholder metadata
          },
        });
      } catch (mongoError: any) {
        console.warn(
          "⚠️ MongoDB Write Failed (Likely due to local standalone instance needing Replica Set for Prisma):",
          mongoError.message,
        );
        // Continue flow - this is critical for dev environments without full replica sets
      }

      // 6. Generate Learning Path
      await LearningPathService.generatePath(
        userId,
        prediction.predicted_course,
      );

      // 7. Finalize Onboarding Status in Postgres
      await prisma.onboardingProgress.update({
        where: { userId },
        data: {
          assessmentComplete: true,
          careerRecommended: true,
          pathGenerated: true,
          status: "COMPLETED",
          completedAt: new Date(),
          currentStep: 5,
        },
      });

      return {
        success: true,
        prediction: prediction,
        predictionId: predictionId,
      };
    } catch (error: any) {
      console.error("MLService - PredictCareer Error:", error);
      throw error;
    }
  }
}
