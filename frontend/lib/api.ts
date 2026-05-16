const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export type Tier = "hot" | "warm" | "cold";

export type DecisionMaker = {
  name: string;
  title: string | null;
  email: string | null;
  email_candidates: string[];
  email_domain_verified: boolean;
};

export type Lead = {
  name: string;
  address: string | null;
  phone: string | null;
  website: string | null;
  rating: number | null;
  review_count: number | null;
  place_id: string;
  decision_makers: DecisionMaker[];
};

export type Touch = {
  day_offset: number;
  purpose: string;
  subject: string | null;
  body: string;
};

export type OutreachSequence = {
  touches: Touch[];
};

export type LeadScore = {
  score: number;
  tier: Tier;
  reasons: string[];
};

export type LeadWithOutreach = {
  lead: Lead;
  outreach: OutreachSequence;
  score: LeadScore | null;
};

export type LeadSearchResponse = {
  business_type: string;
  location: string;
  count: number;
  leads: LeadWithOutreach[];
};

export type ICPQuery = {
  query: string;
  max_results?: number;
};

export async function searchLeadsFromICP(
  query: ICPQuery,
  signal?: AbortSignal
): Promise<LeadSearchResponse> {
  const response = await fetch(`${API_BASE_URL}/leads/icp/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(query),
    signal,
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Search failed (${response.status}): ${detail}`);
  }
  return response.json();
}
