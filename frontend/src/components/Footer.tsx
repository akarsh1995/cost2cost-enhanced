import { Typography } from "@material-tailwind/react";
import TelegramLogo from "./Logos";

export default function SimpleFooter() {
  return (
    <footer className="flex w-full flex-row flex-wrap items-center justify-center gap-y-6 gap-x-12 border-t border-blue-gray-50 py-6 text-center md:justify-between p-5">
      <Typography color="blue-gray" className="font-normal">
        &copy; 2023 Akarsh Jain
      </Typography>
      <ul className="flex flex-wrap items-center gap-y-2 gap-x-8">
        <li>
          <div className="flex items-center space-x-6">
            <div>To add get new features to this web page click {"=>"}</div>
            <a
              target="_blank"
              rel="noopener noreferrer"
              href="https://t.me/akarsh1995"
            >
              <TelegramLogo className="block h-10 w-10" />
            </a>
          </div>
        </li>
      </ul>
    </footer>
  );
}
