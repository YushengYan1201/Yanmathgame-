
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { useTheme } from "@/hooks/use-theme";
import brain from "brain";
import {
  Award,
  FunctionSquareIcon,
  Plus,
  SquareIcon,
  Triangle,
} from "lucide-react";
import type React from "react";
import { useCallback, useEffect, useState } from "react";

// Updated MathQuestion interface
export interface MathQuestion {
  question: string;
  answer?: string;
  topic: "algebra" | "geometry" | "trigonometry" | "arithmetic" | "calculus";
  difficulty: "easy" | "medium" | "hard";
  points: number;
}

const isValidMathQuestion = (data: any): data is MathQuestion => {
  if (
    typeof data === "object" &&
    data !== null &&
    typeof data.question === "string" &&
    (typeof data.answer === "string" || data.answer === undefined) &&
    typeof data.topic === "string" &&
    ["algebra", "geometry", "trigonometry", "arithmetic", "calculus"].includes(
      data.topic,
    ) &&
    typeof data.difficulty === "string" &&
    ["easy", "medium", "hard"].includes(data.difficulty) &&
    typeof data.points === "number"
  ) {
    return true;
  }
  console.error("Invalid question data:", data);
  return false;
};

const topicExplanations = {
  algebra: "Solve equations and manipulate variables.",
  geometry: "Work with shapes, sizes, and positions of figures.",
  trigonometry:
    "Study relationships between side lengths and angles of triangles.",
  arithmetic: "Perform basic mathematical operations with numbers.",
  calculus: "Study continuous change and the rates at which quantities change.",
};

const handleCalculusQuestion = (userAnswer: string, correctAnswer: string) => {
  const options = ["A", "B", "C", "D"];
  return (
    options.includes(userAnswer.toUpperCase()) &&
    userAnswer.toUpperCase() === correctAnswer.toUpperCase()
  );
};

const MathChallengeUI: React.FC = () => {
  const { theme } = useTheme();
  const [question, setQuestion] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string | null>(null);
  const [topic, setTopic] = useState<MathQuestion["topic"] | null>(null);
  const [difficulty, setDifficulty] = useState<
    MathQuestion["difficulty"] | null
  >(null);
  const [points, setPoints] = useState<number | null>(null);
  const [totalScore, setTotalScore] = useState<number>(0);
  const [userAnswer, setUserAnswer] = useState<string>("");
  const [feedback, setFeedback] = useState<string>("");
  const [feedbackType, setFeedbackType] = useState<
    "correct" | "incorrect" | null
  >(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [testResults, setTestResults] = useState<string[]>([]);
  const [questionCounter, setQuestionCounter] = useState<number>(0);
  const [badges, setBadges] = useState<string[]>([]);
  const [consecutiveCorrect, setConsecutiveCorrect] = useState<number>(0);
  const [lastPoints, setLastPoints] = useState<number | null>(null);

  const awardBadges = (score: number, consecutive: number) => {
    const newBadges: string[] = [];
    if (score >= 100 && !badges.includes("Century")) newBadges.push("Century");
    if (score >= 500 && !badges.includes("Math Wizard"))
      newBadges.push("Math Wizard");
    if (consecutive >= 5 && !badges.includes("On Fire"))
      newBadges.push("On Fire");
    if (consecutive >= 10 && !badges.includes("Unstoppable"))
      newBadges.push("Unstoppable");
    if (newBadges.length > 0) {
      setBadges((prevBadges) => [...prevBadges, ...newBadges]);
      setFeedback(
        (prevFeedback) =>
          \`\${prevFeedback} You earned new badge(s): \${newBadges.join(", ")}!\`,
      );
    }
  };

  const fetchQuestion = useCallback(async () => {
    setLoading(true);
    setError(null);
    setUserAnswer("");
    setFeedback("");
    setFeedbackType(null);
    try {
      const response: Response = await brain.get_math_question();
      if (response.status !== 200) {
        throw new Error(\`API returned status \${response.status}\`);
      }
      const data = await response.json();

      if (isValidMathQuestion(data)) {
        setQuestion(data.question);
        setAnswer(data.answer);
        setTopic(data.topic);
        setDifficulty(data.difficulty);
        setPoints(data.points);
        setQuestionCounter((prevCounter) => prevCounter + 1);
      } else {
        throw new TypeError(
          "Invalid or incomplete question data received from the API",
        );
      }
    } catch (err) {
      console.error("Error fetching question:", err);
      if (err instanceof TypeError) {
        setError(
          "Received invalid data from the server. The API response was not as expected. Please try again.",
        );
      } else if (err instanceof Error) {
        if (err.message.includes("404")) {
          setError("Math question not found. Please try again later.");
        } else if (err.message.includes("500")) {
          setError("Server error. Please try again later.");
        } else {
          setError(\`Failed to fetch math question: \${err.message}\`);
        }
      } else {
        setError(
          "An unexpected error occurred while fetching the math question",
        );
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchQuestion();
  }, [fetchQuestion]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (!answer) throw new Error("No answer available for comparison");

      let isCorrect = false;
      if (topic === "algebra" || topic === "arithmetic") {
        isCorrect =
          userAnswer.trim().toLowerCase() === answer.trim().toLowerCase();
      } else if (topic === "calculus") {
        isCorrect = handleCalculusQuestion(userAnswer, answer || "");
      } else {
        const userNum = Number.parseFloat(userAnswer);
        const answerNum = answer ? Number.parseFloat(answer) : Number.NaN;
        if (isNaN(userNum) || isNaN(answerNum)) {
          throw new Error("Invalid numeric input for comparison");
        }
        isCorrect = Math.abs(userNum - answerNum) < 0.01;
      }

      if (isCorrect) {
        const newScore = totalScore + (points || 0);
        const newConsecutive = consecutiveCorrect + 1;
        setFeedback(\`Correct! You earned \${points} points.\`);
        setFeedbackType("correct");
        setTotalScore(newScore);
        setConsecutiveCorrect(newConsecutive);
        setLastPoints(points);
        awardBadges(newScore, newConsecutive);
      } else {
        setFeedback(
          answer
            ? \`Incorrect. The correct answer is \${answer}\`
            : "Incorrect. Please try again.",
        );
        setFeedbackType("incorrect");
        setConsecutiveCorrect(0);
      }
      setTimeout(() => {
        fetchQuestion();
      }, 2000); // 2 seconds delay before fetching a new question
    } catch (err) {
      console.error("Error handling answer submission:", err);
      if (err instanceof Error) {
        setError(\`Error processing answer: \${err.message}\`);
      } else {
        setError("An unknown error occurred while processing your answer");
      }
      setFeedbackType(null);
    }
  };
