import { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SettingsIcon from '@mui/icons-material/Settings';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import SchoolIcon from '@mui/icons-material/School';

export default function AdminDashboard() {
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      // TODO: Implement file upload API call
      console.log('Uploading file:', file.name);
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('Файл успешно загружен (демо режим)');
    } catch (error) {
      console.error('Upload error:', error);
      alert('Ошибка при загрузке файла');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Панель администратора
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Управление системой диагностики
        </Typography>
      </Box>

      {/* Main Action Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Upload Organizations */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <CloudUploadIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Загрузка организаций</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Загрузите Excel-файл со списком организаций (ИНН, наименование, тип, регион)
              </Typography>
              <input
                accept=".xlsx,.xls"
                style={{ display: 'none' }}
                id="upload-excel"
                type="file"
                onChange={handleFileUpload}
              />
              <label htmlFor="upload-excel">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<CloudUploadIcon />}
                  disabled={uploading}
                >
                  {uploading ? 'Загрузка...' : 'Выбрать файл'}
                </Button>
              </label>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SettingsIcon sx={{ mr: 1, color: 'secondary.main' }} />
                <Typography variant="h6">Настройки ИИ</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Управление промптами, моделями и параметрами генерации
              </Typography>
              <Button variant="outlined" disabled>
                Скоро доступно
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Question Generation */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SchoolIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Генерация вопросов</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Создание тестовых вопросов на основе нормативных документов
              </Typography>
              <Button variant="outlined" disabled>
                Скоро доступно
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Analytics */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AnalyticsIcon sx={{ mr: 1, color: 'secondary.main' }} />
                <Typography variant="h6">Аналитика</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Отчёты, кластеризация и образовательные программы
              </Typography>
              <Button variant="outlined" disabled>
                Скоро доступно
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Info */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Быстрая информация
          </Typography>
          <Divider sx={{ my: 2 }} />
          <List>
            <ListItem>
              <ListItemText
                primary="Статус системы"
                secondary="Работает в штатном режиме"
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Этап разработки"
                secondary="Этап 1: Базовая инфраструктура и вход по ИНН"
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Доступный функционал"
                secondary="Вход руководителей по ИНН, просмотр профиля, загрузка организаций"
              />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    </Container>
  );
}
