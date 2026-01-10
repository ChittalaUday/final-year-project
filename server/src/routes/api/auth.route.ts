import { Router } from "express";
import authController from "../../controllers/auth.controller.js";
import {validate} from "../../middleware/validate.middleware.js";
import { validateLogin, validateRegister } from "../../validations/auth.validate.js";
const authRoutes = Router();

authRoutes.post("/login", validate(validateLogin), authController.login);
authRoutes.post("/register", validate(validateRegister), authController.register);

export default authRoutes;
