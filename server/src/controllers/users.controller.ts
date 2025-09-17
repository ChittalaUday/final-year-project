import prisma from "../config/db.postgres.js";
import type { Request, Response } from "express";

const userController = {
  async getUsers(req: Request, res: Response) {
    try {
      const data = await prisma.user.findMany();
      throw Error("Test Err");
      res.json({ data: data });
    } catch (err) {
      console.error("❌ Error in fetching Users Data: ", err);
      res.status(500).json({
        success: true,
      });
    }
  },
};

export default userController;
