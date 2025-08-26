import './globals.css';
import { Inter } from 'next/font/google';
import SplashScreen from './page';
import LoginModal from '../components/LoginModal';
import HomeScreen from '../components/HomeScreen';
import PersonSelectScreen from '../components/PersonSelectScreen';
import DivinationSelectScreen from '../components/DivinationSelectScreen';
import InformationInputScreen from '../components/InformationInputScreen';
import ResultScreen from '../components/ResultScreen';
import MyPage from '../components/MyPage';

const inter = Inter({ subsets: ['latin'] });

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
    <html lang="en">
      <body className={inter.className}>
        <SplashScreen />
        <LoginModal />
        <HomeScreen />
        <PersonSelectScreen />
        <DivinationSelectScreen />
        <InformationInputScreen />
        <ResultScreen />
        <MyPage />
        {children}
      </body>
    </html>
  );
}
