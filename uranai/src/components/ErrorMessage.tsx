"use client";

interface ErrorMessageProps {
  message: string;
  onClose?: () => void;
}

const ErrorMessage = ({ message, onClose }: ErrorMessageProps) => {
  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center">
      <span>{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          className="ml-4 text-white hover:text-red-200 transition-colors"
        >
          <i data-lucide="x" className="w-5 h-5"></i>
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
