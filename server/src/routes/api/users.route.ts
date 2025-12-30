import { Router } from "express";
import userController from "../../controllers/users.controller.js";
import { authenticate } from "../../middleware/authController.js";
const userRoutes = Router();

userRoutes.get("/", userController.getUsers);

userRoutes.use(authenticate);
userRoutes.post("/", userController.createUser);

export default userRoutes;
