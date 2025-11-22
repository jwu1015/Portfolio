import { defineCollection, z } from "astro:content";

const projects = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    date: z.string().or(z.date()).optional(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    cover: z.string().optional(),
    links: z.object({
      demo: z.string().url().optional(),
      code: z.string().url().optional(),
    }).partial().default({}),
    published: z.boolean().default(true),
  }),
});

export const collections = { projects };