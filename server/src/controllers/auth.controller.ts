import prisma from "../config/db.postgres.js";
import type { Request, Response } from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

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
        return res.status(401).json({
          success: false,
          message: "Invalid email or password",
        });
      }

      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
         return res.status(401).json({
          success: false,
          message: "Invalid email or password",
        });
      }
      
      const token = jwt.sign(
          { id: user.id, email: user.email, role: user.role },
          process.env.JWT_SECRET || "my_jwt_scret",
          { expiresIn: "10d" }
      );

      const { password: _, ...userWithoutPassword } = user;

      return res.json({
        success: true,
        message: "Login successful",
        token,
        data: userWithoutPassword,
      });
    } catch (error) {
        console.error("Login Error:", error);
        return res.status(500).json({
            success: false,
            message: "Internal Server Error"
        });
    }
  },

  async register(req: Request, res: Response) {
      try {
            const { name, email, password, dob } = req.body;
            
            const existingUser = await prisma.user.findUnique({ where: { email } });
            if (existingUser) {
                return res.status(400).json({
                    success: false,
                    message: "User already exists",
                });
            }
            
            const hashedPassword = await bcrypt.hash(password, 10);
            
            const newUser = await prisma.user.create({
                data: {
                    name, 
                    email, 
                    password: hashedPassword,
                    dob: new Date(dob),
                }
            });
            
             const token = jwt.sign(
                { id: newUser.id, email: newUser.email, role: newUser.role },
                process.env.JWT_SECRET || "my_jwt_scret",
                { expiresIn: "10d" }
            );

            const { password: _, ...userWithoutPassword } = newUser;

            return res.status(201).json({
                success: true,
                message: "User registered successfully",
                token,
                data: userWithoutPassword
            });

      } catch(error) {
          console.error("Register error:", error);
         return res.status(500).json({ success: false, message: "Internal server error" });
      }
  }
};

export default authController;
