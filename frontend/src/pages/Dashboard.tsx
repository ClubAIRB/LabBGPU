import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  CircularProgress,
  Divider,
  Chip,
} from '@mui/material';
import { authApi, headApi, TestSession } from '../services/apiServices';
import { useAuthStore } from '../store/authStore';
import SchoolIcon from '@mui/icons-material/School';
import PersonIcon from '@mui/icons-material/Person';
import EventIcon from '@mui/icons-material/Event';
import AssessmentIcon from '@mui/icons-material/Assessment';

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  
  const [loading, setLoading] = useState(true);
  const [testSessions, setTestSessions] = useState<TestSession[]>([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [profile, sessions] = await Promise.all([
        authApi.getCurrentHead(),
        headApi.getTestSessions({ limit: 5 }),
      ]);
      
      setTestSessions(sessions);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  const organization = user?.organization;
  const lastTest = testSessions.length > 0 ? testSessions[0] : null;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1">
          Личный кабинет
        </Typography>
        <Button variant="outlined" onClick={handleLogout}>
          Выйти
        </Button>
      </Box>

      {/* Organization Info Card */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SchoolIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Организация</Typography>
              </Box>
              <Typography variant="body1" fontWeight="bold">
                {organization?.name || 'Не указано'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ИНН: {organization?.inn}
              </Typography>
              <Chip 
                label={organization?.type === 'school' ? 'Школа' : 
                       organization?.type === 'kindergarten' ? 'Детский сад' : 
                       'Доп. образование'}
                size="small"
                sx={{ mt: 1 }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PersonIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Руководитель</Typography>
              </Box>
              <Typography variant="body1" fontWeight="bold">
                {user?.full_name || 'Не указано'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user?.created_at ? `В системе с ${new Date(user.created_at).toLocaleDateString('ru-RU')}` : ''}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Action Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <AssessmentIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Пройти тестирование
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Диагностика компетенций руководителя
              </Typography>
              <Button 
                variant="contained" 
                size="large"
                onClick={() => navigate('/test')}
                disabled
              >
                Скоро доступно
              </Button>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <EventIcon sx={{ fontSize: 60, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Результаты
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Просмотр и выгрузка результатов
              </Typography>
              <Button 
                variant="outlined" 
                size="large"
                disabled={!lastTest}
              >
                Скачать PDF
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Last Test Results */}
      {lastTest && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Последнее тестирование
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Дата прохождения
                </Typography>
                <Typography variant="body1">
                  {new Date(lastTest.test_date).toLocaleDateString('ru-RU', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  ID сессии
                </Typography>
                <Typography variant="body1">
                  #{lastTest.id}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {!lastTest && (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="body1" color="text.secondary">
              Вы ещё не проходили тестирование
            </Typography>
          </CardContent>
        </Card>
      )}
    </Container>
  );
}
