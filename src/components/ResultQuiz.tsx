import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function ResultQuiz({ result, total }: any) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Results</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-6">
        <h3>Overall {(result.score / 25) * 100}%</h3>
        <p>
          <strong>Total Questions:</strong> <span>{total}</span>
        </p>
        <p>
          <strong>Total Score:</strong> <span>{result.score}</span>
        </p>
        <p>
          <strong>Correct Answers:</strong> <span>{result.correctAnswers}</span>
        </p>
        <p>
          <strong>Wrong Answers:</strong> <span>{result.wrongAnswers}</span>
        </p>
      </CardContent>
      <CardFooter>
        <Button className="w-full" onClick={() => window.location.reload()}>
          Restart
        </Button>
      </CardFooter>
    </Card>
  );
}
