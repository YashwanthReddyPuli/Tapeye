import type { Metadata } from "next";
import "./globals.css";
import Sidenavbar from "@/components/Sidenavbar";

export const metadata: Metadata = {
  title: "TapEye | Produce Quality Assessment",
  description: "Dual-modal acoustic and visual late-fusion produce grading system.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#121110] text-[#faf9f5] antialiased selection:bg-[#b05730] selection:text-white">
        <Sidenavbar>
          {children}
        </Sidenavbar>
      </body>
    </html>
  );
}

