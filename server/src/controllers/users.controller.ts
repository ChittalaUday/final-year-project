import prisma from "../config/db.postgres.js";
import type { Request, Response } from "express";

const userController = {
  async login(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      
      const data = await prisma.user.findFirst(email);
      res.json(data);
    } catch (error) {}
  },
  async getUsers(req: Request, res: Response) {
    try {
      const data = await prisma.user.findMany();
      res.json({ data: data });
    } catch (err) {
      console.error("❌ Error in fetching Users Data: ", err);
      res.status(500).json({
        success: true,
      });
    }
  },
  async createUser(req: Request, res: Response) {},
};

export default userController;
