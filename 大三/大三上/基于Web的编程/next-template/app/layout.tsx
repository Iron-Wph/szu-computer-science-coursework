'use client'
import router from "next/router";
// app/layout.tsx
import "./globals.css";
import { Button, Link, Navbar, NavbarBrand, NavbarContent, NavbarItem, NextUIProvider } from "@nextui-org/react";
import MyNavBar from "@/components/MyNavBar";
import { Toaster } from "react-hot-toast";
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (
    <html lang="en">
      <body>
        <NextUIProvider>
          <main className="flex-1 min-h-[calc(110vh)] text-foreground mx-auto bg-background">
            <MyNavBar />
            {children}
            <Toaster position="bottom-center"/>
          </main>
        </NextUIProvider>
      </body>
    </html>
  );
}
