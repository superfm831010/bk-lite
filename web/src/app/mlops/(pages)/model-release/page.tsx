import { redirect } from "next/navigation";

export default function HomePage() {
  redirect('/mlops/model-release/list');
}