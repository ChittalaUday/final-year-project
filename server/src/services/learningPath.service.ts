import { postgres as prisma } from "../config/db.js";

export class LearningPathService {
  /**
   * Generates a structural learning path for a user based on their predicted career.
   */
  static async generatePath(userId: string, careerTitle: string) {
    try {
      // 1. Template Definitions for Common Careers (Can be expanded)
      const templates: Record<string, { modules: string[]; duration: number }> =
        {
          "B.Tech": {
            modules: [
              "Introduction to Computer Science",
              "Programming Fundamentals (Python/C++)",
              "Mathematics for Engineering",
              "Data Structures & Algorithms",
              "Web Development Foundations",
            ],
            duration: 16,
          },
          "B.Sc": {
            modules: [
              "Scientific Foundations",
              "Analytical Thinking",
              "Statistics & Probability",
              "Research Methodologies",
              "Domain-Specific Elective",
            ],
            duration: 12,
          },
          MCA: {
            modules: [
              "Advanced Programming Concepts",
              "Database Management Systems",
              "Software Project Management",
              "Full Stack Development",
              "Cloud Computing Basics",
            ],
            duration: 14,
          },
          BCA: {
            modules: [
              "Digital Electronics",
              "Object-Oriented Programming",
              "Operating Systems",
              "Networking Fundamentals",
              "Management Information Systems",
            ],
            duration: 12,
          },
          default: {
            modules: [
              "Core Industry Skills",
              "Communication & Soft Skills",
              "Critical Thinking",
              "Digital Literacy",
              "Personalized Growth Plan",
            ],
            duration: 10,
          },
        };

      const template = templates[careerTitle] || templates["default"];
      if (!template) throw new Error("Learning path template not found.");

      // 2. Create Learning Path in the 'lms' schema
      const path = await prisma.learningPath.create({
        data: {
          userId,
          pathName: `Roadmap to ${careerTitle}`,
          description: `This personalized learning path is designed to bridge the gap between your current skills and a successful career in ${careerTitle}.`,
          targetCareer: careerTitle,
          difficultyLevel: "Beginner",
          estimatedDuration: template.duration, // in weeks
        },
      });

      // 3. Create Modules for the Path
      const moduleData = template.modules.map((title, index) => ({
        pathId: path.id,
        title,
        orderIndex: index + 1,
        description: `Module focused on mastering ${title} concepts and practical applications.`,
        estimatedTime: 480, // 8 hours per module
      }));

      for (const data of moduleData) {
        await prisma.learningModule.create({ data });
      }

      return path;
    } catch (error) {
      console.error("LearningPathService - GeneratePath Error:", error);
      throw error;
    }
  }
}
