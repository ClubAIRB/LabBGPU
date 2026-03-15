import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormLabel,
  TextField,
  Grid,
  Step,
  StepLabel,
  Stepper,
  Paper,
  Alert,
  CircularProgress,
} from '@mui/material';
import { headApi } from '../services/apiServices';

interface Question {
  id: number;
  category: string;
  question_text: string;
  answer_variants: string[];
}

interface Case {
  id: number;
  case_text: string;
}

export default function TestPage() {
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [cases, setCases] = useState<Case[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [caseAnswers, setCaseAnswers] = useState<Record<number, string>>({});
  const [currentStep, setCurrentStep] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [scores, setScores] = useState<Record<string, number> | null>(null);

  useEffect(() => {
    loadTest();
  }, []);

  const loadTest = async () => {
    try {
      // TODO: Call API to get test questions and cases
      // For demo, using placeholder data
      const demoQuestions: Question[] = [
        {
          id: 1,
          category: 'кадры',
          question_text: 'Какой документ является основным при планировании работы с кадрами?',
          answer_variants: [
            'Штатное расписание',
            'План повышения квалификации',
            'Должностные инструкции',
            'Все перечисленные'
          ]
        },
        {
          id: 2,
          category: 'процессы',
          question_text: 'Что входит в основные управленческие процессы?',
          answer_variants: [
            'Планирование и организация',
            'Контроль и анализ',
            'Принятие решений',
            'Все перечисленные'
          ]
        },
        {
          id: 3,
          category: 'результаты',
          question_text: 'Какой показатель наиболее важен для оценки эффективности образовательной организации?',
          answer_variants: [
            'Успеваемость обучающихся',
            'Удовлетворённость родителей',
            'Профессиональный рост педагогов',
            'Комплекс всех показателей'
          ]
        }
      ];

      const demoCases: Case[] = [
        {
          id: 1,
          case_text: `Ситуация: В вашей школе сложилась конфликтная ситуация между двумя учителями-предметниками. 
          Конфликт начался с профессиональных разногласий, но перерос в личную неприязнь. 
          Это начинает сказываться на учебном процессе и атмосфере в коллективе.
          
          Вопрос: Опишите ваши действия как руководителя в данной ситуации.`
        }
      ];

      setQuestions(demoQuestions);
      setCases(demoCases);
    } catch (error) {
      console.error('Error loading test:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId: number, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleCaseAnswerChange = (caseId: number, value: string) => {
    setCaseAnswers(prev => ({ ...prev, [caseId]: value }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      // Convert answers to format expected by API
      const answersData = Object.fromEntries(
        Object.entries(answers).map(([key, value]) => [key, value])
      );
      
      const caseAnswersData = Object.fromEntries(
        Object.entries(caseAnswers).map(([key, value]) => [String(key), value])
      );

      // TODO: Call actual API
      // const result = await headApi.submitTestSession({
      //   answers: answersData,
      //   case_answers: caseAnswersData
      // });
      
      // Demo response
      const result = {
        scores: {
          'кадры': 85,
          'процессы': 75,
          'результаты': 90
        }
      };
      
      setScores(result.scores);
      setCompleted(true);
    } catch (error) {
      console.error('Error submitting test:', error);
      alert('Ошибка при отправке ответов');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetry = () => {
    setAnswers({});
    setCaseAnswers({});
    setCurrentStep(0);
    setCompleted(false);
    setScores(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (completed) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Card>
          <CardContent sx={{ textAlign: 'center' }}>
            <Typography variant="h4" gutterBottom>
              Тестирование завершено!
            </Typography>
            <Alert severity="success" sx={{ my: 3 }}>
              Ваши ответы успешно сохранены
            </Alert>
            
            {scores && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Результаты по категориям:
                </Typography>
                <Grid container spacing={2} justifyContent="center">
                  {Object.entries(scores).map(([category, score]) => (
                    <Grid item xs={12} sm={4} key={category}>
                      <Paper sx={{ p: 2, bgcolor: score >= 80 ? 'success.light' : score >= 60 ? 'warning.light' : 'error.light' }}>
                        <Typography variant="body2" textTransform="capitalize">
                          {category}
                        </Typography>
                        <Typography variant="h4">
                          {score}%
                        </Typography>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            )}
            
            <Box sx={{ mt: 4 }}>
              <Button 
                variant="contained" 
                onClick={() => navigate('/dashboard')}
                sx={{ mr: 2 }}
              >
                Вернуться в личный кабинет
              </Button>
              <Button 
                variant="outlined" 
                onClick={handleRetry}
              >
                Пройти заново
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Container>
    );
  }

  const totalSteps = questions.length + cases.length;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Тестирование руководителя
      </Typography>
      <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
        Ответьте на вопросы и выполните кейсы
      </Typography>

      <Stepper activeStep={currentStep} sx={{ mb: 4 }}>
        {questions.map((q, index) => (
          <Step key={`q-${q.id}`}>
            <StepLabel>Вопрос {index + 1}</StepLabel>
          </Step>
        ))}
        {cases.map((c, index) => (
          <Step key={`c-${c.id}`}>
            <StepLabel>Кейс {index + 1}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Card>
        <CardContent>
          {/* Questions */}
          {currentStep < questions.length && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Вопрос {currentStep + 1} из {questions.length}
              </Typography>
              <Typography variant="body1" sx={{ mb: 3 }}>
                Категория: <strong>{questions[currentStep].category}</strong>
              </Typography>
              
              <FormLabel component="legend">
                {questions[currentStep].question_text}
              </FormLabel>
              
              <RadioGroup
                value={answers[questions[currentStep].id] || ''}
                onChange={(e) => handleAnswerChange(questions[currentStep].id, e.target.value)}
                sx={{ mt: 2 }}
              >
                {questions[currentStep].answer_variants.map((variant, idx) => (
                  <FormControlLabel
                    key={idx}
                    value={variant}
                    control={<Radio />}
                    label={variant}
                  />
                ))}
              </RadioGroup>

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
                <Button
                  disabled={currentStep === 0}
                  onClick={() => setCurrentStep(prev => prev - 1)}
                >
                  Назад
                </Button>
                <Button
                  variant="contained"
                  disabled={!answers[questions[currentStep].id]}
                  onClick={() => setCurrentStep(prev => prev + 1)}
                >
                  {currentStep === questions.length - 1 ? 'К кейсам' : 'Далее'}
                </Button>
              </Box>
            </Box>
          )}

          {/* Cases */}
          {currentStep >= questions.length && currentStep < totalSteps && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Кейс {currentStep - questions.length + 1} из {cases.length}
              </Typography>
              
              <Paper sx={{ p: 3, mb: 3, bgcolor: 'grey.50' }}>
                <Typography variant="body1" whiteSpace="pre-line">
                  {cases[currentStep - questions.length].case_text}
                </Typography>
              </Paper>
              
              <TextField
                fullWidth
                multiline
                rows={6}
                placeholder="Ваш ответ..."
                value={caseAnswers[cases[currentStep - questions.length].id] || ''}
                onChange={(e) => handleCaseAnswerChange(cases[currentStep - questions.length].id, e.target.value)}
              />

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
                <Button
                  onClick={() => setCurrentStep(prev => prev - 1)}
                >
                  Назад
                </Button>
                <Button
                  variant="contained"
                  disabled={!caseAnswers[cases[currentStep - questions.length].id]}
                  onClick={() => {
                    if (currentStep === totalSteps - 1) {
                      handleSubmit();
                    } else {
                      setCurrentStep(prev => prev + 1);
                    }
                  }}
                >
                  {currentStep === totalSteps - 1 ? 'Завершить тестирование' : 'Далее'}
                </Button>
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>

      {submitting && (
        <Box sx={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, bgcolor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 9999 }}>
          <Card sx={{ p: 4, textAlign: 'center' }}>
            <CircularProgress sx={{ mb: 2 }} />
            <Typography>Отправка ответов...</Typography>
          </Card>
        </Box>
      )}
    </Container>
  );
}
