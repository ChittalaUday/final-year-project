import { Router } from "express";
import {
  compareImages,
  uploadImages,
  getApiInfo,
} from "../../controllers/clip.controller.js";

const clipRoutes = Router();

// Get API information
clipRoutes.get("/info", getApiInfo);

// Compare images endpoint
clipRoutes.post("/compare", uploadImages, compareImages);

export default clipRoutes;
