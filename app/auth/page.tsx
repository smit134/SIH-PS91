"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Lock, Phone, ArrowRight, Sparkles, KeyRound, ShieldCheck, Mail, AlertCircle, CheckCircle2 } from "lucide-react";
import { useAuth } from "@/app/context/AuthContext";

type AuthTab = "password" | "otp";

export default function AuthPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading, loginWithPassword, registerWithPassword, sendOtp, verifyOtp } = useAuth();

  // Mode selection
  const [tab, setTab] = useState<AuthTab>("password");
  const [isLogin, setIsLogin] = useState(true);

  // Form fields
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("+91 98765 43210");
  const [password, setPassword] = useState("secretPass123");
  const [email, setEmail] = useState("");

  // OTP specific state
  const [otpCode, setOtpCode] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otpCountdown, setOtpCountdown] = useState(0);

  // Status & error states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // If already logged in, redirect to dashboard
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      const hasProfile = typeof window !== "undefined" && localStorage.getItem("thinkforge_profile");
      if (hasProfile) {
        router.push("/dashboard");
      } else {
        router.push("/register");
      }
    }
  }, [isAuthenticated, authLoading, router]);

  // OTP Countdown timer
  useEffect(() => {
    if (otpCountdown > 0) {
      const timer = setTimeout(() => setOtpCountdown(otpCountdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [otpCountdown]);

  const cleanPhone = (p: string) => {
    const digits = p.replace(/[^0-9+]/g, "");
    if (!digits.startsWith("+")) {
      return `+91${digits.replace(/^0+/, "")}`;
    }
    return digits;
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      const trimmedInput = phone.trim();

      if (isLogin) {
        if (!trimmedInput) {
          throw new Error("Please enter your mobile number or email address.");
        }
        let identifier = trimmedInput;
        if (trimmedInput.includes("@")) {
          identifier = trimmedInput.toLowerCase();
        } else {
          identifier = cleanPhone(trimmedInput);
          if (identifier.length < 10) {
            throw new Error("Please enter a valid 10-digit mobile number.");
          }
        }

        await loginWithPassword(identifier, password);
        setSuccessMsg("Signed in successfully! Redirecting...");
      } else {
        const formattedPhone = cleanPhone(phone);
        if (formattedPhone.length < 10) {
          throw new Error("Please enter a valid 10-digit mobile number.");
        }
        if (!name.trim()) {
          throw new Error("Please enter your full name.");
        }
        if (password.length < 6) {
          throw new Error("Password must be at least 6 characters.");
        }
        await registerWithPassword(name.trim(), formattedPhone, password, email);
        setSuccessMsg("Account created! Redirecting to setup...");
      }

      // Check redirection destination
      const hasProfile = typeof window !== "undefined" && localStorage.getItem("thinkforge_profile");
      setTimeout(() => {
        if (hasProfile) {
          router.push("/dashboard");
        } else {
          router.push("/register");
        }
      }, 700);
    } catch (err: any) {
      console.warn("Authentication check:", err?.message);
      setError(err?.message || "Invalid mobile number/email or password.");
    } finally {
      setLoading(false);
    }
  };

  const handleSendOtp = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      const formattedPhone = cleanPhone(phone);
      if (formattedPhone.length < 10) {
        throw new Error("Please enter a valid 10-digit mobile number.");
      }

      const res = await sendOtp(formattedPhone);
      setOtpSent(true);
      setOtpCountdown(res.expiresInSeconds || 300);
      setSuccessMsg(res.message || `OTP sent to ${formattedPhone}. Please check your phone for the 6-digit code.`);
    } catch (err: any) {
      console.warn("OTP send error:", err);
      setError(err?.message || "Failed to dispatch OTP. Please check your number.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      const formattedPhone = cleanPhone(phone);
      if (!otpCode || otpCode.trim().length < 4) {
        throw new Error("Please enter the 6-digit verification code.");
      }

      await verifyOtp(formattedPhone, otpCode.trim(), name.trim() || undefined);
      setSuccessMsg("Phone verified successfully! Redirecting...");

      const hasProfile = typeof window !== "undefined" && localStorage.getItem("thinkforge_profile");
      setTimeout(() => {
        if (hasProfile) {
          router.push("/dashboard");
        } else {
          router.push("/register");
        }
      }, 700);
    } catch (err: any) {
      console.error("OTP verify error:", err);
      setError(err?.message || "Invalid or expired OTP code.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4 relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 left-1/3 w-80 h-80 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-slate-900/90 backdrop-blur-xl border border-slate-800/90 rounded-3xl p-8 shadow-2xl relative z-10">
        {/* Brand Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-500/20 to-teal-500/20 text-brand-400 border border-brand-500/30 mb-3 shadow-glow-teal">
            <Sparkles className="w-6 h-6 text-brand-400" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Think<span className="text-brand-400">Forge</span>
          </h1>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 mt-1">
            Rural Enterprise Intelligence Platform
          </p>
        </div>

        {/* Tab Toggle: Password vs Mobile OTP */}
        <div className="flex rounded-xl bg-slate-950 p-1 mb-6 border border-slate-800">
          <button
            type="button"
            onClick={() => {
              setTab("password");
              setError(null);
            }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
              tab === "password"
                ? "bg-slate-800 text-white shadow-sm border border-slate-700"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Lock className="w-3.5 h-3.5" />
            Password Auth
          </button>
          <button
            type="button"
            onClick={() => {
              setTab("otp");
              setError(null);
            }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
              tab === "otp"
                ? "bg-slate-800 text-white shadow-sm border border-slate-700"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <KeyRound className="w-3.5 h-3.5 text-brand-400" />
            Mobile OTP
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-5 p-3.5 rounded-xl bg-red-950/50 border border-red-800/80 text-red-300 text-xs flex items-start gap-2.5 animate-fadeIn">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Success Alert */}
        {successMsg && (
          <div className="mb-5 p-3.5 rounded-xl bg-emerald-950/50 border border-emerald-800/80 text-emerald-300 text-xs flex items-start gap-2.5 animate-fadeIn">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* --- TAB 1: PASSWORD AUTH (LOGIN / REGISTER) --- */}
        {tab === "password" && (
          <form onSubmit={handlePasswordSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">Full Name *</label>
                <div className="relative">
                  <div className="absolute left-3.5 top-3 w-4 h-4 text-slate-500 flex items-center justify-center font-bold text-xs">
                    Aa
                  </div>
                  <input
                    type="text"
                    required={!isLogin}
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Lakshmi Devi"
                    className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all placeholder:text-slate-600"
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">
                {isLogin ? "Mobile Number or Email *" : "Mobile Phone Number *"}
              </label>
              <div className="relative">
                {isLogin && phone.includes("@") ? (
                  <Mail className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
                ) : (
                  <Phone className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
                )}
                <input
                  type={isLogin ? "text" : "tel"}
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder={isLogin ? "98765 43210 or ramesh@example.org" : "+91 98765 43210"}
                  className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all placeholder:text-slate-600"
                />
              </div>
            </div>

            {!isLogin && (
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">Email Address (Optional)</label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="lakshmi@example.org"
                    className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all placeholder:text-slate-600"
                  />
                </div>
              </div>
            )}

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-medium text-slate-300">Password *</label>
                {isLogin && (
                  <button
                    type="button"
                    onClick={() => {
                      setTab("otp");
                      setOtpSent(false);
                    }}
                    className="text-[11px] text-brand-400 hover:text-brand-300"
                  >
                    Forgot password? Use OTP
                  </button>
                )}
              </div>
              <div className="relative">
                <Lock className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all placeholder:text-slate-600"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-brand-600 to-teal-600 text-white hover:opacity-95 shadow-glow-teal transition-all disabled:opacity-50 cursor-pointer"
            >
              {loading ? (
                <span>Authenticating...</span>
              ) : (
                <>
                  <span>{isLogin ? "Sign In with Password" : "Create Account & Continue"}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>

            {isLogin && (
              <div className="mt-3 p-2.5 rounded-lg bg-slate-800/40 border border-slate-800 text-[11px] text-slate-400 flex items-start gap-2">
                <span className="text-brand-400 font-bold">Tip:</span>
                <span>
                  If you signed in via OTP or forgot your password, switch to the{" "}
                  <button
                    type="button"
                    onClick={() => {
                      setTab("otp");
                      setOtpSent(false);
                    }}
                    className="text-brand-400 underline font-medium hover:text-brand-300"
                  >
                    Mobile OTP tab
                  </button>{" "}
                  for instant SMS login without needing a password.
                </span>
              </div>
            )}

            <div className="pt-2 text-center text-xs text-slate-400">
              {isLogin ? "Don't have an account yet?" : "Already registered?"}
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin);
                  setError(null);
                  setSuccessMsg(null);
                }}
                className="ml-1.5 text-brand-400 hover:text-brand-300 font-semibold transition-colors"
              >
                {isLogin ? "Sign up" : "Sign in"}
              </button>
            </div>
          </form>
        )}

        {/* --- TAB 2: MOBILE OTP AUTH (INSTANT ONBOARDING) --- */}
        {tab === "otp" && (
          <div className="space-y-4">
            {!otpSent ? (
              <form onSubmit={handleSendOtp} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">Mobile Phone Number</label>
                  <div className="relative">
                    <Phone className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
                    <input
                      type="tel"
                      required
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+91 98765 43210"
                      className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all placeholder:text-slate-600"
                    />
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1.5">
                    We will send a 6-digit verification code to this mobile number.
                  </p>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-brand-600 to-teal-600 text-white hover:opacity-95 shadow-glow-teal transition-all disabled:opacity-50 cursor-pointer"
                >
                  {loading ? "Sending Code..." : "Send Verification Code (OTP)"}
                  {!loading && <ArrowRight className="w-4 h-4" />}
                </button>
              </form>
            ) : (
              <form onSubmit={handleVerifyOtp} className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="text-xs font-medium text-slate-300">Enter 6-Digit OTP</label>
                    {otpCountdown > 0 && (
                      <span className="text-[11px] text-slate-400">
                        Expires in: <strong className="text-brand-400 font-mono">{otpCountdown}s</strong>
                      </span>
                    )}
                  </div>
                  <div className="relative">
                    <KeyRound className="absolute left-3.5 top-3 w-4 h-4 text-brand-400" />
                    <input
                      type="text"
                      required
                      maxLength={6}
                      value={otpCode}
                      onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ""))}
                      placeholder="••••••"
                      autoFocus
                      className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-brand-500/50 text-white text-center text-lg tracking-widest font-mono focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 transition-all placeholder:text-slate-700"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">
                    Your Name (for new entrepreneurs)
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Lakshmi Devi"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 transition-all placeholder:text-slate-600"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-brand-600 to-teal-600 text-white hover:opacity-95 shadow-glow-teal transition-all disabled:opacity-50 cursor-pointer"
                >
                  {loading ? "Verifying..." : "Verify & Enter ThinkForge"}
                  {!loading && <ArrowRight className="w-4 h-4" />}
                </button>

                <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                  <button
                    type="button"
                    onClick={() => setOtpSent(false)}
                    className="text-slate-400 hover:text-slate-200"
                  >
                    ← Change phone number
                  </button>
                  <button
                    type="button"
                    disabled={otpCountdown > 0 || loading}
                    onClick={() => handleSendOtp()}
                    className={`font-semibold ${
                      otpCountdown > 0 ? "text-slate-600 cursor-not-allowed" : "text-brand-400 hover:text-brand-300"
                    }`}
                  >
                    {otpCountdown > 0 ? `Resend in ${otpCountdown}s` : "Resend OTP"}
                  </button>
                </div>
              </form>
            )}
          </div>
        )}

        {/* Security & Verification Footer */}
        <div className="mt-8 pt-4 border-t border-slate-800/80 flex items-center justify-center gap-2 text-[11px] text-slate-500">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
          <span>PostgreSQL JWT Sessions & Encrypted Credentials</span>
        </div>
      </div>
    </div>
  );
}
