import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import ShellWrapper from "@/components/ShellWrapper";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "ThinkForge — AI Rural Business Advisory & Financial Structuring (SIH26091)",
  description:
    "AI-driven hyper-local rural entrepreneurship decision-support platform for micro-entrepreneurs. Feasibility, partners, financial structuring & government schemes.",
};

import AiAssistant from "./components/AiAssistant";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased bg-slate-50 text-slate-900 min-h-screen">
        <ShellWrapper>{children}</ShellWrapper>
        <AiAssistant />
      </body>
    </html>
  );
}
