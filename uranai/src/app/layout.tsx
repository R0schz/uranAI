import './globals.css';
import { Noto_Sans_JP, Shippori_Mincho } from 'next/font/google';
import { AppProvider } from '../contexts/AppContext';

const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  weight: ['300', '400', '700'],
});

const shipporiMincho = Shippori_Mincho({
  subsets: ['latin'],
  weight: ['400', '700'],
});

export const metadata = {
  title: 'uranAI',
  description: 'AI Fortune Telling App',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className={`${notoSansJP.className} antialiased`}>
        <AppProvider>
          {children}
        </AppProvider>
      </body>
    </html>
  );
}