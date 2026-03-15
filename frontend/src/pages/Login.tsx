import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import { authApi } from '../services/apiServices';
import { useAuthStore } from '../store/authStore';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  
  const [inn, setInn] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // Validate INN length
      if (inn.length < 10 || inn.length > 12) {
        throw new Error('ИНН должен содержать от 10 до 12 цифр');
      }

      const response = await authApi.headLogin(inn);
      
      // Store token and user data
      login(response.access_token, response.head);
      
      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Ошибка при входе');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Card sx={{ width: '100%', p: 2 }}>
          <CardContent>
            <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mb: 3 }}>
              ИИ-Эксперт
            </Typography>
            
            <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
              Диагностика руководителей образовательных организаций
            </Typography>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="ИНН организации"
                value={inn}
                onChange={(e) => setInn(e.target.value.replace(/\D/g, ''))}
                placeholder="Введите ИНН вашей организации"
                margin="normal"
                required
                inputProps={{ 
                  maxLength: 12,
                  pattern: '[0-9]*'
                }}
                disabled={loading}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Войти'}
              </Button>
            </form>

            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                Для администраторов:{' '}
                <a href="/admin/login" style={{ color: '#1976d2' }}>
                  Войти как администратор
                </a>
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
}
