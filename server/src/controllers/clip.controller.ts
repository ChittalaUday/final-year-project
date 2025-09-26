// src/routes/clip.route.ts

import type { Request, Response } from "express";
import multer from "multer";
import path from "path";
import fs from "fs";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

// Multer configuration for file uploads
const upload = multer({
  dest: "uploads/",
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith("image/")) {
      cb(null, true);
    } else {
      cb(null, false);
    }
  },
});

// Interface for typed request
export interface CompareImagesRequest extends Request {
  files?: {
    image1?: Express.Multer.File[];
    image2?: Express.Multer.File[];
  };
  body: { tag?: string };
}

// Upload middleware
export const uploadImages = upload.fields([
  { name: "image1", maxCount: 1 },
  { name: "image2", maxCount: 1 },
]);

// Compare images endpoint
export const compareImages = async (
  req: CompareImagesRequest,
  res: Response
) => {
  try {
    const files = req.files as { [key: string]: Express.Multer.File[] };
    const { tag } = req.body;

    if (!files?.image1?.[0] || !files?.image2?.[0]) {
      return res.status(400).json({
        success: false,
        message: "Both image1 and image2 are required",
      });
    }

    const image1Path = path.resolve(files.image1[0].path);
    const image2Path = path.resolve(files.image2[0].path);

    // Python executable & script
    const pythonPath = path.join(
      process.cwd(),
      "python-env",
      "Scripts",
      "python.exe"
    );
    const scriptPath = path.join(
      process.cwd(),
      "python-scripts",
      "clip_compare_flexible.py"
    );

    let cmd = `"${pythonPath}" "${scriptPath}" "${image1Path}" "${image2Path}"`;
    if (tag) cmd += ` "${tag}"`;

    const { stdout, stderr } = await execAsync(cmd);

    // Clean up uploaded files
    try {
      fs.unlinkSync(image1Path);
      fs.unlinkSync(image2Path);
    } catch (cleanupError) {
      console.error("Error cleaning up files:", cleanupError);
    }

    if (stderr) {
      console.error("Python stderr:", stderr);
      return res.status(500).json({
        success: false,
        message: "Python execution error",
        error: stderr,
      });
    }

    // Parse JSON output from Python
    let result;
    try {
      result = JSON.parse(stdout);
    } catch (err) {
      console.error("JSON parse error:", err, "stdout:", stdout);
      return res
        .status(500)
        .json({ success: false, message: "Invalid JSON from Python script" });
    }

    return res.status(200).json({
      success: true,
      message: "Image comparison completed",
      data: result,
    });
  } catch (error) {
    console.error("compareImages error:", error);

    // Cleanup files on error
    try {
      const files = req.files as { [key: string]: Express.Multer.File[] };
      if (files?.image1?.[0]) fs.unlinkSync(files.image1[0].path);
      if (files?.image2?.[0]) fs.unlinkSync(files.image2[0].path);
    } catch (cleanupError) {
      console.error("Error cleaning up files after error:", cleanupError);
    }

    return res.status(500).json({
      success: false,
      message: error instanceof Error ? error.message : "Unknown error",
    });
  }
};

// Optional: API info endpoint
export const getApiInfo = (req: Request, res: Response) => {
  const info = {
    description:
      "Compare two images for similarity using CLIP (Contrastive Language-Image Pre-training)",
    supported_formats: ["JPEG", "PNG", "GIF", "BMP", "WebP"],
    max_file_size: "10MB per image",
    endpoints: {
      "POST /api/clip/compare": {
        description: "Compare two images with optional text tag",
        required_fields: ["image1", "image2"],
        optional_fields: ["tag"],
        response: {
          image_similarity: "float (0-1)",
          text_similarity: "float (0-1, if tag provided)",
          decision: "string with match result",
          details: "string with similarity info",
        },
      },
      "GET /api/clip/info": {
        description: "Get API information and usage details",
      },
    },
  };

  return res
    .status(200)
    .json({ success: true, message: "CLIP API information", data: info });
};
