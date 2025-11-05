import Image from "next/image";
import { Button } from "@/components/ui/button";
import Header from "@/components/home/header";
import api from "@/lib/axios";

export const revalidate = 43200;

export default async function Home() {

  return (
    <div className="min-h-screen bg-primary/3">
      <Header />
    </div>
  );
}
