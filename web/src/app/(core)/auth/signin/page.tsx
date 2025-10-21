import { getAuthOptions } from "@/constants/authOptions";
import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import SigninClient from "./SigninClient";

// Note: Error messages are now handled through i18n in SigninClient component
// These are fallback error messages for when i18n is not available
const signinErrors: Record<string | "default", string> = {
  default: "auth.errors.default",
  signin: "auth.errors.signin",
  oauthsignin: "auth.errors.oauthsignin",
  oauthcallbackerror: "auth.errors.oauthcallbackerror",
  oauthcreateaccount: "auth.errors.oauthcreateaccount",
  emailcreateaccount: "auth.errors.emailcreateaccount",
  callback: "auth.errors.callback",
  oauthaccountnotlinked: "auth.errors.oauthaccountnotlinked",
  sessionrequired: "auth.errors.sessionrequired",
};

interface SignInPageProp {
  params?: object;
  searchParams: {
    callbackUrl: string;
    error: string;
  };
}

export default async function SigninPage({ searchParams }: SignInPageProp) {
  const authOptions = await getAuthOptions();
  const session = await getServerSession(authOptions);
  if (session && session.user && session.user.id) {
    redirect(searchParams.callbackUrl || "/");
  }
  return <SigninClient searchParams={searchParams} signinErrors={signinErrors} />;
}
