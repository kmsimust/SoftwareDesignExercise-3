"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user) {
      router.push('/library');
    }
  }, [router]);

  return (
    <div>
      <h1>Ya, It's landing page.</h1>
      <Link href="/signup">
        <button>Sign Up</button>
      </Link>
      <Link href="/login">
        <button>Login</button>
      </Link>
    </div>
  );
}
