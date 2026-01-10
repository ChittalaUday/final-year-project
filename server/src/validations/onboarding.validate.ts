import Joi from "joi";

export const setAgeGroupSchema = Joi.object({
  ageGroup: Joi.string()
    .valid("CHILD", "SCHOOL", "COLLEGE", "GRADUATE", "PROFESSIONAL")
    .required()
    .messages({
      "any.only": "Invalid age group",
      "string.empty": "Age group is required",
    }),
});

export const updateProfileSchema = Joi.object({
  schoolName: Joi.string().allow(null, ""),
  grade: Joi.number().integer().allow(null),
  collegeName: Joi.string().allow(null, ""),
  course: Joi.string().allow(null, ""),
  specialization: Joi.string().allow(null, ""),
  currentYear: Joi.number().integer().allow(null),
  cgpaPercentage: Joi.number().allow(null),
  highestEducation: Joi.string().allow(null, ""),
  yearsOfExperience: Joi.number().allow(null),
  currentJobTitle: Joi.string().allow(null, ""),
  currentCompany: Joi.string().allow(null, ""),
  currentIndustry: Joi.string().allow(null, ""),
  totalExperience: Joi.number().allow(null),
  domainShiftIntent: Joi.boolean().allow(null),
  targetDomain: Joi.string().allow(null, ""),
});

export const setInterestsSchema = Joi.object({
  interestIds: Joi.array().items(Joi.string().uuid()).required().messages({
    "array.base": "interestIds must be an array",
    "string.uuid": "Invalid interest ID format",
  }),
});

export const setSkillsSchema = Joi.object({
  skills: Joi.array()
    .items(
      Joi.object({
        skillId: Joi.string().uuid().required(),
        proficiencyLevel: Joi.number().integer().min(1).max(5).default(1),
      }),
    )
    .required()
    .messages({
      "array.base": "skills must be an array",
    }),
});
