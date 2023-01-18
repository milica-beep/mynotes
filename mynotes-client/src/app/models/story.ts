import { Category } from "./category";

export class Story {
    id!: string;
    title!: string;
    text!: string;
    timestamp!: Date;
    grade!: Number;
    writer!: any;
    category!: Category;
  }