```typescript
type Author = {
  slug: string;
  name: string;
  url: string;
  description: string;
};

type Editor = {
  slug: string;
  name: string;
  url: string;
  description: string;
};

type Category = {
  name: string;
  slug: string;
  taxonomy: string;
};

type Tag = {
  name: string;
  slug: string;
  taxonomy: string;
};

type PrimaryCategory = {
  name: string;
  url: string;
  description: string;
  slug: string;
  taxonomy: string;
};

type RelatedToken = {
  ID: string;
  name: string;
  symbol: string;
  url: string;
};

type ArticleData = {
  id: string;
  url: string;
  type: string;
  title: string;
  slug: string;
  label: string;
  published: string;
  publishedTimestamp: string;
  publishedFormatted: string;
  publishedFormattedShort: string;
  publishedFormattedMid: string;
  modified: string;
  byLines: string;
  authors: Author[];
  editors: Editor[];
  thumbnail: string;
  thumbnailCredit: string;
  thumbnailCaption: string;
  intro: string;
  excerpt: string;
  body: string;
  primaryCategory: PrimaryCategory;
  categories: Category[];
  tags: Tag[];
  wordCount: string;
  readingTime: string;
  priority: number;
  relatedTokens: RelatedToken[];
};
```
