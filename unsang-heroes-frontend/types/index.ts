export type User = {
  id: number,
  username: string,
  email: string,
}

export interface HeroAvatar {
  small?: string;
  medium?: string;
  large?: string;
}

export interface StoryCover {
  small?: string;
  medium?: string;
  large?: string;
}

export const HERO_STATUS_LIST = [
  'under_review',
  'verified',
  'rejected',
  'archived',
  'draft',
];
export type HeroStatus = typeof HERO_STATUS_LIST[number];

export const STORY_STATUS_LIST = [
  'published',
  'draft',
  'pending',
];
export type StoryStatus = typeof STORY_STATUS_LIST[number];


export interface StorySummary {
  id: number;
  title: string;
  hero_name: string;
  hero_avatar: HeroAvatar;
  story_cover: StoryCover;
  hero_quote?: string;
  intro: string;
  status: StoryStatus;
  impact_location: string;
}
