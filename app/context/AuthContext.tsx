"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { useRouter, usePathname } from "next/navigation";
import { apiFetch, ApiError } from "@/lib/api";

export interface UserSummary {
  id: string;
  phone: string;
  email?: string | null;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  full_name?: string | null;
}

export interface AuthContextType {
  user: UserSummary | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  loginWithPassword: (phone: string, password: string) => Promise<void>;
  registerWithPassword: (
    fullName: string,
    phone: string,
    password: string,
    email?: string,
    language?: string
  ) => Promise<void>;
  sendOtp: (phone: string) => Promise<{ message: string; expiresInSeconds: number; isRegistered: boolean }>;
  verifyOtp: (phone: string, otpCode: string, fullName?: string, language?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserSummary | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const router = useRouter();
  const pathname = usePathname();

  // Helper to persist auth tokens & user
  const handleAuthSuccess = (accessToken: string, refreshToken: string, userData: any, customName?: string) => {
    localStorage.setItem("thinkforge_access_token", accessToken);
    localStorage.setItem("thinkforge_refresh_token", refreshToken);
    // Backward compatibility for existing endpoints
    localStorage.setItem("thinkforge_token", userData.id);

    const displayName = customName || userData.full_name || userData.phone || "Rural Entrepreneur";
    localStorage.setItem("thinkforge_name", displayName);

    const mappedUser: UserSummary = {
      id: userData.id,
      phone: userData.phone,
      email: userData.email,
      role: userData.role || "ENTREPRENEUR",
      is_active: userData.is_active ?? true,
      is_verified: userData.is_verified ?? true,
      full_name: displayName,
    };

    setToken(accessToken);
    setUser(mappedUser);
  };

  // Check auth session on load
  const loadUserSession = useCallback(async () => {
    const savedToken = typeof window !== "undefined" ? localStorage.getItem("thinkforge_access_token") : null;
    const savedName = typeof window !== "undefined" ? localStorage.getItem("thinkforge_name") : null;
    const legacyToken = typeof window !== "undefined" ? localStorage.getItem("thinkforge_token") : null;

    if (!savedToken && !legacyToken) {
      setIsLoading(false);
      return;
    }

    if (savedToken) {
      try {
        const data = await apiFetch("/api/v1/auth/me", {
          headers: { Authorization: `Bearer ${savedToken}` },
        });

        if (data && data.user) {
          setUser({
            ...data.user,
            full_name: data.profile_summary?.full_name || savedName || data.user.phone,
          });
          setToken(savedToken);
        }
      } catch (err) {
        console.warn("Session verification failed, attempting refresh or fallback:", err);
        // Fallback to legacy mock session if stored
        if (legacyToken) {
          setUser({
            id: legacyToken,
            phone: "+919876543210",
            role: "ENTREPRENEUR",
            is_active: true,
            is_verified: true,
            full_name: savedName || "Ramesh Kumar",
          });
        }
      }
    } else if (legacyToken) {
      // Legacy session compatibility
      setUser({
        id: legacyToken,
        phone: "+919876543210",
        role: "ENTREPRENEUR",
        is_active: true,
        is_verified: true,
        full_name: savedName || "Ramesh Kumar",
      });
    }

    setIsLoading(false);
  }, []);

  useEffect(() => {
    loadUserSession();
  }, [loadUserSession]);

  // 1. Password Login
  const loginWithPassword = async (identifier: string, password: string) => {
    let cleanIdentifier = identifier.trim();
    if (!cleanIdentifier.includes("@") && !cleanIdentifier.startsWith("+")) {
      const digits = cleanIdentifier.replace(/[^0-9]/g, "");
      if (digits.length === 10) {
        cleanIdentifier = `+91${digits}`;
      }
    }

    const res = await apiFetch("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({
        phone: cleanIdentifier,
        password: password,
      }),
    });

    handleAuthSuccess(res.access_token, res.refresh_token, res.user);
  };

  // 2. Password Registration
  const registerWithPassword = async (
    fullName: string,
    phone: string,
    password: string,
    email?: string,
    language: string = "en"
  ) => {
    const formattedPhone = phone.startsWith("+") ? phone : `+91${phone.replace(/^0+/, "")}`;
    const res = await apiFetch("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({
        full_name: fullName,
        phone: formattedPhone,
        password: password,
        email: email && email.trim().length > 0 ? email.trim() : null,
        language: language,
        role: "ENTREPRENEUR",
      }),
    });

    handleAuthSuccess(res.access_token, res.refresh_token, res.user, fullName);
  };

  // 3. Dispatch OTP to phone
  const sendOtp = async (phone: string) => {
    const formattedPhone = phone.startsWith("+") ? phone : `+91${phone.replace(/^0+/, "")}`;
    const res = await apiFetch("/api/v1/auth/otp/send", {
      method: "POST",
      body: JSON.stringify({ phone: formattedPhone }),
    });

    return {
      message: res.message,
      expiresInSeconds: res.expires_in_seconds,
      isRegistered: res.is_registered_user,
    };
  };

  // 4. Verify OTP and login/auto-onboard
  const verifyOtp = async (phone: string, otpCode: string, fullName?: string, language: string = "en") => {
    const formattedPhone = phone.startsWith("+") ? phone : `+91${phone.replace(/^0+/, "")}`;
    const res = await apiFetch("/api/v1/auth/otp/verify", {
      method: "POST",
      body: JSON.stringify({
        phone: formattedPhone,
        otp_code: otpCode,
        full_name: fullName || "Rural Entrepreneur",
        language: language,
      }),
    });

    handleAuthSuccess(res.access_token, res.refresh_token, res.user, fullName);
  };

  // 5. Sign Out
  const logout = () => {
    localStorage.removeItem("thinkforge_access_token");
    localStorage.removeItem("thinkforge_refresh_token");
    localStorage.removeItem("thinkforge_token");
    setToken(null);
    setUser(null);
    router.push("/auth");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        loginWithPassword,
        registerWithPassword,
        sendOtp,
        verifyOtp,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
