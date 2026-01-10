import { postgres as prisma } from "../config/db.js";
import type { Request, Response } from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { sendResponse } from "../utils/customResponse.js";

const authController = {
  async login(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      const user = await prisma.user.findFirst({
        where: {
          email: email,
        },
      });

      if (!user) {
        return sendResponse(res, false, "Invalid email or password", 401);
      }

      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return sendResponse(res, false, "Invalid email or password", 401);
      }

      const token = jwt.sign(
        { id: user.id, email: user.email, role: user.role },
        process.env.JWT_SECRET || "my_jwt_scret",
        { expiresIn: "10d" },
      );

      const { password: _, ...userWithoutPassword } = user;

      return sendResponse(res, true, "Login successful", 200, {
        token,
        user: userWithoutPassword,
      });
    } catch (error) {
      console.error("Login Error:", error);
      return sendResponse(res, false, "Internal Server Error", 500);
    }
  },

  async register(req: Request, res: Response) {
    try {
      const { name, email, password, dob } = req.body;

      const existingUser = await prisma.user.findUnique({ where: { email } });
      if (existingUser) {
        return sendResponse(res, false, "User already exists", 400);
      }

      const hashedPassword = await bcrypt.hash(password, 10);

      // Use a transaction to ensure User, UserProfile, and OnboardingProgress are created together
      const newUser = await prisma.$transaction(async (tx) => {
        const user = await tx.user.create({
          data: {
            name,
            email,
            password: hashedPassword,
          },
        });

        await tx.userProfile.create({
          data: {
            userId: user.id,
            dateOfBirth: dob ? new Date(dob) : null,
          },
        });

        await tx.onboardingProgress.create({
          data: {
            userId: user.id,
            status: "NOT_STARTED",
            currentStep: 0,
            totalSteps: 5, // Default total steps
          },
        });

        return user;
      });

      const token = jwt.sign(
        { id: newUser.id, email: newUser.email, role: newUser.role },
        process.env.JWT_SECRET || "my_jwt_scret",
        { expiresIn: "10d" },
      );

      const { password: _, ...userWithoutPassword } = newUser;

      return sendResponse(res, true, "User registered successfully", 201, {
        token,
        user: userWithoutPassword,
      });
    } catch (error) {
      console.error("Register error:", error);
      return sendResponse(res, false, "Internal server error", 500);
    }
  },
};

export default authController;
