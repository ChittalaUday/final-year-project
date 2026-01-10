import type { Request,Response,NextFunction } from "express";
import Joi from "joi";

export const validate = (schema:Joi.ObjectSchema) => {
    return (req:Request,res:Response,next:NextFunction) => {
        const {error,value}=schema.validate(req.body || {},{abortEarly:false});
        if(error){
            res.status(400).json({
                success:false,
                message:error.details?.map((detail)=>detail.message)|| "Invalid request data" ,
            });
            return;
        }
        req.body=value;
        next();
    }
}