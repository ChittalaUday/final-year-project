import { postgres as prisma } from "../config/db.js";
import type { Request, Response } from "express";
import { MLService } from "../services/ml.service.js";
import { sendResponse } from "../utils/customResponse.js";

export const onboardingController = {
  // GET /api/onboarding/status
  async getStatus(req: Request, res: Response) {
    try {
      const userId = (req.user as any).id;
      const progress = await prisma.onboardingProgress.findUnique({
        where: { userId },
      });

      if (!progress) {
        return sendResponse(res, false, "Onboarding progress not found", 404);
      }

      return sendResponse(res, true, "Status retrieved", 200, progress);
    } catch (error) {
      console.error("GetStatus error:", error);
      return sendResponse(res, false, "Internal server error", 500);
    }
  },

  // POST /api/onboarding/age-group
  async setAgeGroup(req: Request, res: Response) {
    try {
      const userId = (req.user as any).id;
      const { ageGroup } = req.body;

      // Note: Validation is now handled by Joi middleware.

      await prisma.$transaction([
        prisma.onboardingProgress.update({
          where: { userId },
          data: {
            ageGroup: ageGroup as any,
            ageDetected: true,
            currentStep: 1,
          },
        }),
        prisma.learnerProfile.upsert({
          where: { userId },
          update: { ageGroup: ageGroup as any },
          create: { userId, ageGroup: ageGroup as any },
        }),
      ]);

      return sendResponse(res, true, "Age group set successfully");
    } catch (error) {
      console.error("SetAgeGroup error:", error);
      return sendResponse(res, false, "Internal server error", 500);
    }
  },

  // POST /api/onboarding/profile
  async updateProfile(req: Request, res: Response) {
    try {
      const userId = (req.user as any).id;
      const profileData = req.body;

      // Note: In production, we should validate fields required for specific AgeGroups.
      await prisma.learnerProfile.update({
        where: { userId },
        data: {
          schoolName: profileData.schoolName,
          grade: profileData.grade,
          collegeName: profileData.collegeName,
          course: profileData.course,
          specialization: profileData.specialization,
          currentYear: profileData.currentYear,
          cgpaPercentage: profileData.cgpaPercentage,
          highestEducation: profileData.highestEducation,
          yearsOfExperience: profileData.yearsOfExperience,
          currentJobTitle: profileData.currentJobTitle,
          currentCompany: profileData.currentCompany,
          currentIndustry: profileData.currentIndustry,
          totalExperience: profileData.totalExperience,
          domainShiftIntent: profileData.domainShiftIntent,
          targetDomain: profileData.targetDomain,
        },
      });

      await prisma.onboardingProgress.update({
        where: { userId },
        data: {
          roleSelected: true,
          currentStep: 2,
        },
      });

      return sendResponse(res, true, "Profile updated successfully");
    } catch (error) {
      console.error("UpdateProfile error:", error);
      return sendResponse(res, false, "Internal server error", 500);
    }
  },

  // POST /api/onboarding/interests
  async setInterests(req: Request, res: Response) {
    try {
      const userId = (req.user as any).id;
      const { interestIds } = req.body;

      if (!Array.isArray(interestIds)) {
        return res
          .status(400)
          .json({ success: false, message: "interestIds must be an array" });
      }

      const learnerProfile = await prisma.learnerProfile.findUnique({
        where: { userId },
      });
      if (!learnerProfile) {
        return sendResponse(res, false, "Profile not found", 404);
      }

      await prisma.$transaction([
        prisma.learnerInterest.deleteMany({
          where: { learnerProfileId: learnerProfile.id },
        }),
        prisma.learnerInterest.createMany({
          data: interestIds.map((id: string) => ({
            learnerProfileId: learnerProfile.id,
            interestId: id,
          })),
        }),
        prisma.onboardingProgress.update({
          where: { userId },
          data: {
            interestsCollected: true,
            currentStep: 3,
          },
        }),
      ]);

      return sendResponse(res, true, "Interests saved successfully");
    } catch (error) {
      console.error("SetInterests error:", error);
      return res
        .status(500)
        .json({ success: false, message: "Internal server error" });
    }
  },

  // POST /api/onboarding/skills
  async setSkills(req: Request, res: Response) {
    try {
      const userId = (req.user as any).id;
      const { skills } = req.body;

      if (!Array.isArray(skills)) {
        return res
          .status(400)
          .json({ success: false, message: "skills must be an array" });
      }

      const learnerProfile = await prisma.learnerProfile.findUnique({
        where: { userId },
      });
      if (!learnerProfile) {
        return sendResponse(res, false, "Profile not found", 404);
      }

      await prisma.$transaction([
        prisma.learnerSkill.deleteMany({
          where: { learnerProfileId: learnerProfile.id },
        }),
        prisma.learnerSkill.createMany({
          data: skills.map((s: any) => ({
            learnerProfileId: learnerProfile.id,
            skillId: s.skillId,
            proficiencyLevel: s.proficiencyLevel || 1,
          })),
        }),
        prisma.onboardingProgress.update({
          where: { userId },
          data: {
            skillsCollected: true,
            currentStep: 4,
          },
        }),
      ]);

      return sendResponse(res, true, "Skills saved successfully");
    } catch (error) {
      console.error("SetSkills error:", error);
      return res
        .status(500)
        .json({ success: false, message: "Internal server error" });
    }
  },

  // POST /api/onboarding/complete
  async finalize(req: Request, res: Response) {
    try {
      const userId = (req.user as any).id;

      const result = await MLService.predictCareer(userId);

      return sendResponse(res, true, "Assessment completed", 200, result);
    } catch (error: any) {
      console.error("Finalize error:", error);
      return sendResponse(
        res,
        false,
        error.message || "Internal server error",
        500,
      );
    }
  },
};
