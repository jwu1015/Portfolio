import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    summary: z.string().max(280),
    cover: z.string().url(),
    tags: z.array(z.string()).default([]),
    demoUrl: z.string().url().optional(),
    codeUrl: z.string().url().optional(),
    published: z.boolean().default(true),
  }),
});

export const collections = { projects };
