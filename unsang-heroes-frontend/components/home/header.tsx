"use client"

import { Heart } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

export default function Header() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Stories" },
    { href: "/share", label: "Share a Stroy" },
    { href: "/community", label: "Our Community" },
  ]

  return (
    <nav className="fixed top-0 w-full bg-primary/1 backdrop-blur-sm border-b border-primary/20 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="flex items-center space-x-2">
              <Heart className="w-6 h-6 text-primary fill-current" />
              <h2 className="text-2xl font-bold text-gray-700 font-[Merriweather]">
                UnsungHeroes
              </h2>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            {links.map(({ href, label }) => {
              const isActive = pathname === href;

              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    "font-medium pb-1",
                    isActive
                      ? "text-primary border-b-2 border-primary"
                      : "text-foregroud hover:text-primary"
                  )}
                >
                  {label}
                </Link>)
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
