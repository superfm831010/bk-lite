import { getServerSession } from "next-auth/next";
import { redirect } from "next/navigation";
import { authOptions } from "@/constants/authOptions";
import ResetPasswordClient from "./ResetPasswordClient";

export default async function ResetPasswordPage() {
  const session = await getServerSession(authOptions);
  
  // If no session or user, redirect to login
  if (!session || !session.user) {
    redirect("/auth/signin");
  }
  
  // If user doesn't have temporary password flag, redirect to home
  // (They shouldn't be here if they don't need to reset password)
  if (!session.user.temporary_pwd) {
    redirect("/");
  }

  return <ResetPasswordClient username={session.user.username || "Guest"} />;
}
