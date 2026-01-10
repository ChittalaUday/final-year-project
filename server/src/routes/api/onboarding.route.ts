import { Router } from "express";
import { onboardingController } from "../../controllers/onboarding.controller.js";
import { authenticate } from "../../middleware/auth.middleware.js";
import { validate } from "../../middleware/validate.middleware.js";
import {
  setAgeGroupSchema,
  updateProfileSchema,
  setInterestsSchema,
  setSkillsSchema,
} from "../../validations/onboarding.validate.js";

const onboardingRoutes = Router();

// All onboarding routes require authentication
onboardingRoutes.use(authenticate);

onboardingRoutes.get("/status", onboardingController.getStatus);
onboardingRoutes.post(
  "/age-group",
  validate(setAgeGroupSchema),
  onboardingController.setAgeGroup,
);
onboardingRoutes.post(
  "/profile",
  validate(updateProfileSchema),
  onboardingController.updateProfile,
);
onboardingRoutes.post(
  "/interests",
  validate(setInterestsSchema),
  onboardingController.setInterests,
);
onboardingRoutes.post(
  "/skills",
  validate(setSkillsSchema),
  onboardingController.setSkills,
);
onboardingRoutes.post("/finalize", onboardingController.finalize);

export default onboardingRoutes;
