-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "core";

-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "lms";

-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "ml";

-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "onboarding";

-- CreateEnum
CREATE TYPE "core"."UserRole" AS ENUM ('LEARNER', 'INSTRUCTOR', 'MENTOR', 'ADMIN', 'INSTITUTION', 'COMPANY');

-- CreateEnum
CREATE TYPE "onboarding"."OnboardingStatus" AS ENUM ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'SKIPPED');

-- CreateEnum
CREATE TYPE "core"."AgeGroup" AS ENUM ('CHILD', 'SCHOOL', 'COLLEGE', 'GRADUATE', 'PROFESSIONAL');

-- CreateEnum
CREATE TYPE "ml"."ConfidenceLevel" AS ENUM ('HIGH', 'MEDIUM', 'LOW', 'INSUFFICIENT');

-- CreateEnum
CREATE TYPE "lms"."ContentType" AS ENUM ('VIDEO', 'ARTICLE', 'QUIZ', 'INTERACTIVE', 'EXERCISE');

-- CreateEnum
CREATE TYPE "lms"."AssessmentType" AS ENUM ('APTITUDE', 'SKILL', 'KNOWLEDGE', 'PRACTICE');

-- CreateTable
CREATE TABLE "core"."User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "name" TEXT,
    "phoneNumber" TEXT,
    "role" "core"."UserRole" NOT NULL DEFAULT 'LEARNER',
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "emailVerified" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "core"."UserProfile" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "avatarUrl" TEXT,
    "bio" TEXT,
    "dateOfBirth" TIMESTAMP(3),
    "gender" TEXT,
    "country" TEXT,
    "city" TEXT,
    "timezone" TEXT,
    "language" TEXT NOT NULL DEFAULT 'en',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "UserProfile_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."OnboardingProgress" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "status" "onboarding"."OnboardingStatus" NOT NULL DEFAULT 'NOT_STARTED',
    "currentStep" INTEGER NOT NULL DEFAULT 0,
    "totalSteps" INTEGER NOT NULL DEFAULT 0,
    "ageGroup" "core"."AgeGroup",
    "roleSelected" BOOLEAN NOT NULL DEFAULT false,
    "ageDetected" BOOLEAN NOT NULL DEFAULT false,
    "interestsCollected" BOOLEAN NOT NULL DEFAULT false,
    "skillsCollected" BOOLEAN NOT NULL DEFAULT false,
    "assessmentComplete" BOOLEAN NOT NULL DEFAULT false,
    "careerRecommended" BOOLEAN NOT NULL DEFAULT false,
    "pathGenerated" BOOLEAN NOT NULL DEFAULT false,
    "completedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "OnboardingProgress_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."LearnerProfile" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "ageGroup" "core"."AgeGroup" NOT NULL,
    "parentEmail" TEXT,
    "parentConsent" BOOLEAN NOT NULL DEFAULT false,
    "schoolName" TEXT,
    "grade" INTEGER,
    "collegeName" TEXT,
    "course" TEXT,
    "specialization" TEXT,
    "currentYear" INTEGER,
    "cgpaPercentage" DOUBLE PRECISION,
    "highestEducation" TEXT,
    "yearsOfExperience" DOUBLE PRECISION,
    "currentJobTitle" TEXT,
    "currentCompany" TEXT,
    "currentIndustry" TEXT,
    "totalExperience" DOUBLE PRECISION,
    "domainShiftIntent" BOOLEAN NOT NULL DEFAULT false,
    "targetDomain" TEXT,
    "certifications" TEXT[],
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LearnerProfile_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."Interest" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "category" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Interest_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."Skill" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "category" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Skill_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."LearnerInterest" (
    "id" TEXT NOT NULL,
    "learnerProfileId" TEXT NOT NULL,
    "interestId" TEXT NOT NULL,
    "priority" INTEGER NOT NULL DEFAULT 1,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "LearnerInterest_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."LearnerSkill" (
    "id" TEXT NOT NULL,
    "learnerProfileId" TEXT NOT NULL,
    "skillId" TEXT NOT NULL,
    "proficiencyLevel" INTEGER NOT NULL DEFAULT 1,
    "isVerified" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LearnerSkill_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "onboarding"."CareerGoal" (
    "id" TEXT NOT NULL,
    "learnerProfileId" TEXT NOT NULL,
    "goalTitle" TEXT NOT NULL,
    "description" TEXT,
    "targetDate" TIMESTAMP(3),
    "priority" INTEGER NOT NULL DEFAULT 1,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "CareerGoal_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ml"."MLPrediction" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "inputFeatures" JSONB NOT NULL,
    "predictedCourse" TEXT,
    "confidence" "ml"."ConfidenceLevel" NOT NULL,
    "confidenceScore" DOUBLE PRECISION NOT NULL,
    "alternativeCareers" TEXT[],
    "alternativeScores" DOUBLE PRECISION[],
    "modelVersion" TEXT NOT NULL,
    "modelType" TEXT NOT NULL DEFAULT 'RandomForest',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "MLPrediction_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ml"."CareerRecommendation" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "predictionId" TEXT NOT NULL,
    "careerTitle" TEXT NOT NULL,
    "careerDescription" TEXT,
    "requiredSkills" TEXT[],
    "educationPath" TEXT[],
    "industryDemand" TEXT,
    "avgSalaryRange" TEXT,
    "isAccepted" BOOLEAN NOT NULL DEFAULT false,
    "isExploring" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "CareerRecommendation_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."LearningPath" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "pathName" TEXT NOT NULL,
    "description" TEXT,
    "targetCareer" TEXT NOT NULL,
    "estimatedDuration" INTEGER,
    "difficultyLevel" TEXT,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "completionPercent" DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LearningPath_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."LearningModule" (
    "id" TEXT NOT NULL,
    "pathId" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "orderIndex" INTEGER NOT NULL,
    "estimatedTime" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LearningModule_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."Content" (
    "id" TEXT NOT NULL,
    "moduleId" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "contentType" "lms"."ContentType" NOT NULL,
    "contentUrl" TEXT,
    "duration" INTEGER,
    "orderIndex" INTEGER NOT NULL,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Content_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."Assessment" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "assessmentType" "lms"."AssessmentType" NOT NULL,
    "duration" INTEGER,
    "passingScore" DOUBLE PRECISION,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Assessment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."Question" (
    "id" TEXT NOT NULL,
    "assessmentId" TEXT NOT NULL,
    "questionText" TEXT NOT NULL,
    "questionType" TEXT NOT NULL,
    "options" TEXT[],
    "correctAnswer" TEXT NOT NULL,
    "explanation" TEXT,
    "points" INTEGER NOT NULL DEFAULT 1,
    "orderIndex" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Question_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."AssessmentResult" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "assessmentId" TEXT NOT NULL,
    "score" DOUBLE PRECISION NOT NULL,
    "maxScore" DOUBLE PRECISION NOT NULL,
    "percentageScore" DOUBLE PRECISION NOT NULL,
    "isPassed" BOOLEAN NOT NULL,
    "timeSpent" INTEGER,
    "answersJson" JSONB NOT NULL,
    "aiAnalysis" TEXT,
    "strengths" TEXT[],
    "weaknesses" TEXT[],
    "recommendations" TEXT[],
    "completedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AssessmentResult_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."Enrollment" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "pathId" TEXT NOT NULL,
    "enrolledAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" TIMESTAMP(3),
    "isActive" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "Enrollment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."LearningProgress" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "contentId" TEXT NOT NULL,
    "isCompleted" BOOLEAN NOT NULL DEFAULT false,
    "progressPercent" DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    "timeSpent" INTEGER NOT NULL DEFAULT 0,
    "lastAccessedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" TIMESTAMP(3),

    CONSTRAINT "LearningProgress_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "lms"."Achievement" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "badgeUrl" TEXT,
    "category" TEXT,
    "points" INTEGER NOT NULL DEFAULT 0,
    "awardedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Achievement_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "core"."InstructorProfile" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "expertise" TEXT[],
    "bio" TEXT,
    "qualifications" TEXT[],
    "yearsOfExperience" DOUBLE PRECISION,
    "isVerified" BOOLEAN NOT NULL DEFAULT false,
    "rating" DOUBLE PRECISION,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "InstructorProfile_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "core"."InstitutionProfile" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "institutionName" TEXT NOT NULL,
    "institutionType" TEXT NOT NULL,
    "address" TEXT,
    "website" TEXT,
    "contactEmail" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "InstitutionProfile_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "core"."Group" (
    "id" TEXT NOT NULL,
    "institutionId" TEXT NOT NULL,
    "groupName" TEXT NOT NULL,
    "description" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Group_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "core"."User"("email");

-- CreateIndex
CREATE INDEX "User_email_idx" ON "core"."User"("email");

-- CreateIndex
CREATE INDEX "User_role_idx" ON "core"."User"("role");

-- CreateIndex
CREATE UNIQUE INDEX "UserProfile_userId_key" ON "core"."UserProfile"("userId");

-- CreateIndex
CREATE INDEX "UserProfile_userId_idx" ON "core"."UserProfile"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "OnboardingProgress_userId_key" ON "onboarding"."OnboardingProgress"("userId");

-- CreateIndex
CREATE INDEX "OnboardingProgress_userId_idx" ON "onboarding"."OnboardingProgress"("userId");

-- CreateIndex
CREATE INDEX "OnboardingProgress_status_idx" ON "onboarding"."OnboardingProgress"("status");

-- CreateIndex
CREATE UNIQUE INDEX "LearnerProfile_userId_key" ON "onboarding"."LearnerProfile"("userId");

-- CreateIndex
CREATE INDEX "LearnerProfile_userId_idx" ON "onboarding"."LearnerProfile"("userId");

-- CreateIndex
CREATE INDEX "LearnerProfile_ageGroup_idx" ON "onboarding"."LearnerProfile"("ageGroup");

-- CreateIndex
CREATE UNIQUE INDEX "Interest_name_key" ON "onboarding"."Interest"("name");

-- CreateIndex
CREATE INDEX "Interest_name_idx" ON "onboarding"."Interest"("name");

-- CreateIndex
CREATE UNIQUE INDEX "Skill_name_key" ON "onboarding"."Skill"("name");

-- CreateIndex
CREATE INDEX "Skill_name_idx" ON "onboarding"."Skill"("name");

-- CreateIndex
CREATE INDEX "LearnerInterest_learnerProfileId_idx" ON "onboarding"."LearnerInterest"("learnerProfileId");

-- CreateIndex
CREATE INDEX "LearnerInterest_interestId_idx" ON "onboarding"."LearnerInterest"("interestId");

-- CreateIndex
CREATE UNIQUE INDEX "LearnerInterest_learnerProfileId_interestId_key" ON "onboarding"."LearnerInterest"("learnerProfileId", "interestId");

-- CreateIndex
CREATE INDEX "LearnerSkill_learnerProfileId_idx" ON "onboarding"."LearnerSkill"("learnerProfileId");

-- CreateIndex
CREATE INDEX "LearnerSkill_skillId_idx" ON "onboarding"."LearnerSkill"("skillId");

-- CreateIndex
CREATE UNIQUE INDEX "LearnerSkill_learnerProfileId_skillId_key" ON "onboarding"."LearnerSkill"("learnerProfileId", "skillId");

-- CreateIndex
CREATE INDEX "CareerGoal_learnerProfileId_idx" ON "onboarding"."CareerGoal"("learnerProfileId");

-- CreateIndex
CREATE INDEX "MLPrediction_userId_idx" ON "ml"."MLPrediction"("userId");

-- CreateIndex
CREATE INDEX "MLPrediction_confidence_idx" ON "ml"."MLPrediction"("confidence");

-- CreateIndex
CREATE INDEX "CareerRecommendation_userId_idx" ON "ml"."CareerRecommendation"("userId");

-- CreateIndex
CREATE INDEX "CareerRecommendation_careerTitle_idx" ON "ml"."CareerRecommendation"("careerTitle");

-- CreateIndex
CREATE INDEX "LearningPath_userId_idx" ON "lms"."LearningPath"("userId");

-- CreateIndex
CREATE INDEX "LearningPath_targetCareer_idx" ON "lms"."LearningPath"("targetCareer");

-- CreateIndex
CREATE INDEX "LearningModule_pathId_idx" ON "lms"."LearningModule"("pathId");

-- CreateIndex
CREATE INDEX "LearningModule_orderIndex_idx" ON "lms"."LearningModule"("orderIndex");

-- CreateIndex
CREATE INDEX "Content_moduleId_idx" ON "lms"."Content"("moduleId");

-- CreateIndex
CREATE INDEX "Content_contentType_idx" ON "lms"."Content"("contentType");

-- CreateIndex
CREATE INDEX "Assessment_assessmentType_idx" ON "lms"."Assessment"("assessmentType");

-- CreateIndex
CREATE INDEX "Question_assessmentId_idx" ON "lms"."Question"("assessmentId");

-- CreateIndex
CREATE INDEX "AssessmentResult_userId_idx" ON "lms"."AssessmentResult"("userId");

-- CreateIndex
CREATE INDEX "AssessmentResult_assessmentId_idx" ON "lms"."AssessmentResult"("assessmentId");

-- CreateIndex
CREATE INDEX "Enrollment_userId_idx" ON "lms"."Enrollment"("userId");

-- CreateIndex
CREATE INDEX "Enrollment_pathId_idx" ON "lms"."Enrollment"("pathId");

-- CreateIndex
CREATE INDEX "LearningProgress_userId_idx" ON "lms"."LearningProgress"("userId");

-- CreateIndex
CREATE INDEX "LearningProgress_contentId_idx" ON "lms"."LearningProgress"("contentId");

-- CreateIndex
CREATE UNIQUE INDEX "LearningProgress_userId_contentId_key" ON "lms"."LearningProgress"("userId", "contentId");

-- CreateIndex
CREATE INDEX "Achievement_userId_idx" ON "lms"."Achievement"("userId");

-- CreateIndex
CREATE INDEX "Achievement_category_idx" ON "lms"."Achievement"("category");

-- CreateIndex
CREATE UNIQUE INDEX "InstructorProfile_userId_key" ON "core"."InstructorProfile"("userId");

-- CreateIndex
CREATE INDEX "InstructorProfile_userId_idx" ON "core"."InstructorProfile"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "InstitutionProfile_userId_key" ON "core"."InstitutionProfile"("userId");

-- CreateIndex
CREATE INDEX "InstitutionProfile_userId_idx" ON "core"."InstitutionProfile"("userId");

-- CreateIndex
CREATE INDEX "Group_institutionId_idx" ON "core"."Group"("institutionId");

-- AddForeignKey
ALTER TABLE "core"."UserProfile" ADD CONSTRAINT "UserProfile_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."OnboardingProgress" ADD CONSTRAINT "OnboardingProgress_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."LearnerProfile" ADD CONSTRAINT "LearnerProfile_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."LearnerInterest" ADD CONSTRAINT "LearnerInterest_learnerProfileId_fkey" FOREIGN KEY ("learnerProfileId") REFERENCES "onboarding"."LearnerProfile"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."LearnerInterest" ADD CONSTRAINT "LearnerInterest_interestId_fkey" FOREIGN KEY ("interestId") REFERENCES "onboarding"."Interest"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."LearnerSkill" ADD CONSTRAINT "LearnerSkill_learnerProfileId_fkey" FOREIGN KEY ("learnerProfileId") REFERENCES "onboarding"."LearnerProfile"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."LearnerSkill" ADD CONSTRAINT "LearnerSkill_skillId_fkey" FOREIGN KEY ("skillId") REFERENCES "onboarding"."Skill"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "onboarding"."CareerGoal" ADD CONSTRAINT "CareerGoal_learnerProfileId_fkey" FOREIGN KEY ("learnerProfileId") REFERENCES "onboarding"."LearnerProfile"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."LearningModule" ADD CONSTRAINT "LearningModule_pathId_fkey" FOREIGN KEY ("pathId") REFERENCES "lms"."LearningPath"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."Content" ADD CONSTRAINT "Content_moduleId_fkey" FOREIGN KEY ("moduleId") REFERENCES "lms"."LearningModule"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."Question" ADD CONSTRAINT "Question_assessmentId_fkey" FOREIGN KEY ("assessmentId") REFERENCES "lms"."Assessment"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."AssessmentResult" ADD CONSTRAINT "AssessmentResult_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."AssessmentResult" ADD CONSTRAINT "AssessmentResult_assessmentId_fkey" FOREIGN KEY ("assessmentId") REFERENCES "lms"."Assessment"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."Enrollment" ADD CONSTRAINT "Enrollment_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."LearningProgress" ADD CONSTRAINT "LearningProgress_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "lms"."Achievement" ADD CONSTRAINT "Achievement_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "core"."InstructorProfile" ADD CONSTRAINT "InstructorProfile_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "core"."InstitutionProfile" ADD CONSTRAINT "InstitutionProfile_userId_fkey" FOREIGN KEY ("userId") REFERENCES "core"."User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "core"."Group" ADD CONSTRAINT "Group_institutionId_fkey" FOREIGN KEY ("institutionId") REFERENCES "core"."InstitutionProfile"("id") ON DELETE CASCADE ON UPDATE CASCADE;
