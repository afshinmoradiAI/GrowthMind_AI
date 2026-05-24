const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export type User = {
  id: string;
  email: string;
  display_name: string | null;
  created_at: string;
};

export type AuthSuccess = { user: User };

export class AuthError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!response.ok) {
    let detail = "";
    try {
      const body = await response.json();
      detail =
        typeof body.detail === "string"
          ? body.detail
          : JSON.stringify(body.detail ?? body);
    } catch {
      detail = await response.text();
    }
    throw new AuthError(detail || `Request failed (${response.status})`, response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export function register(input: {
  email: string;
  password: string;
  display_name?: string;
}): Promise<AuthSuccess> {
  return request<AuthSuccess>("/auth/register", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function login(input: {
  email: string;
  password: string;
}): Promise<AuthSuccess> {
  return request<AuthSuccess>("/auth/login", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function logout(): Promise<void> {
  return request<void>("/auth/logout", { method: "POST" });
}

export async function me(): Promise<User | null> {
  try {
    return await request<User>("/auth/me");
  } catch (err) {
    if (err instanceof AuthError && err.status === 401) return null;
    throw err;
  }
}
