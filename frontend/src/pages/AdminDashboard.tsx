import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  TextField,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Alert,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SettingsIcon from '@mui/icons-material/Settings';
import PsychologyIcon from '@mui/icons-material/Psychology';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import DescriptionIcon from '@mui/icons-material/Description';
import EventIcon from '@mui/icons-material/Event';
import { organizationApi } from '../services/apiServices';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`admin-tabpanel-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [organizations, setOrganizations] = useState<any[]>([]);
  
  // Prompt templates state
  const [prompts, setPrompts] = useState<any[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<any>(null);
  const [promptDialogOpen, setPromptDialogOpen] = useState(false);
  
  // Model settings state
  const [models, setModels] = useState<any[]>([]);
  const [selectedModel, setSelectedModel] = useState<any>(null);
  
  // Questions state
  const [questions, setQuestions] = useState<any[]>([]);
  const [generatingQuestions, setGeneratingQuestions] = useState(false);
  
  // Cases state
  const [cases, setCases] = useState<any[]>([]);
  const [generatingCases, setGeneratingCases] = useState(false);
  
  // Analytics state
  const [analytics, setAnalytics] = useState<any>(null);
  const [clusters, setClusters] = useState<any[]>([]);
  
  // Schedule state
  const [schedule, setSchedule] = useState<any[]>([]);

  useEffect(() => {
    loadOrganizations();
    loadAnalytics();
  }, []);

  const loadOrganizations = async () => {
    try {
      const data = await organizationApi.listOrganizations({ limit: 100 });
      setOrganizations(data);
    } catch (error) {
      console.error('Error loading organizations:', error);
    }
  };

  const loadAnalytics = async () => {
    // TODO: Implement API calls for analytics
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await organizationApi.uploadExcel(file);
      alert('Файл успешно загружен');
      loadOrganizations();
    } catch (error: any) {
      console.error('Upload error:', error);
      alert('Ошибка при загрузке файла: ' + (error.response?.data?.detail || error.message));
    } finally {
      setUploading(false);
    }
  };

  const handleGenerateQuestions = async () => {
    setGeneratingQuestions(true);
    try {
      // TODO: Call API to generate questions
      await new Promise(resolve => setTimeout(resolve, 2000));
      alert('Вопросы сгенерированы (демо)');
    } catch (error) {
      console.error('Generation error:', error);
      alert('Ошибка при генерации вопросов');
    } finally {
      setGeneratingQuestions(false);
    }
  };

  const handleGenerateCases = async () => {
    setGeneratingCases(true);
    try {
      // TODO: Call API to generate cases
      await new Promise(resolve => setTimeout(resolve, 2000));
      alert('Кейсы сгенерированы (демо)');
    } catch (error) {
      console.error('Generation error:', error);
      alert('Ошибка при генерации кейсов');
    } finally {
      setGeneratingCases(false);
    }
  };

  const handleRunClustering = async () => {
    try {
      // TODO: Call API to run clustering
      await new Promise(resolve => setTimeout(resolve, 2000));
      alert('Кластеризация выполнена (демо)');
    } catch (error) {
      console.error('Clustering error:', error);
      alert('Ошибка при кластеризации');
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Панель администратора
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Управление системой диагностики руководителей
        </Typography>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Организации" icon={<CloudUploadIcon />} iconPosition="start" />
          <Tab label="Настройки ИИ" icon={<SettingsIcon />} iconPosition="start" />
          <Tab label="Вопросы" icon={<PsychologyIcon />} iconPosition="start" />
          <Tab label="Кейсы" icon={<DescriptionIcon />} iconPosition="start" />
          <Tab label="Аналитика" icon={<AnalyticsIcon />} iconPosition="start" />
          <Tab label="Календарь" icon={<EventIcon />} iconPosition="start" />
        </Tabs>
      </Box>

      {/* Tab Panel 0: Organizations */}
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Загрузка организаций
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Загрузите Excel-файл со списком организаций (колонки: inn, name, type, region)
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
                    variant="contained"
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

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Список организаций ({organizations.length})
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>ИНН</TableCell>
                        <TableCell>Наименование</TableCell>
                        <TableCell>Тип</TableCell>
                        <TableCell>Регион</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {organizations.slice(0, 10).map((org) => (
                        <TableRow key={org.id}>
                          <TableCell>{org.inn}</TableCell>
                          <TableCell>{org.name || '-'}</TableCell>
                          <TableCell>
                            <Chip 
                              label={org.type === 'school' ? 'Школа' : 
                                     org.type === 'kindergarten' ? 'Детский сад' : 
                                     'Доп. образование'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{org.region || '-'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Tab Panel 1: AI Settings */}
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Промпты для генерации
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Настройка шаблонов промптов для различных категорий
                </Typography>
                <Button variant="outlined" onClick={() => setPromptDialogOpen(true)}>
                  Управление промптами
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Параметры моделей
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Настройка температуры, штрафов и других параметров ИИ
                </Typography>
                <Button variant="outlined" disabled>
                  Скоро доступно
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Модели эмбеддингов
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Выбор модели для семантического сходства
                </Typography>
                <Button variant="outlined" disabled>
                  Скоро доступно
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Порог сходства
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Установка порога для проверки уникальности вопросов
                </Typography>
                <TextField
                  type="number"
                  defaultValue={0.8}
                  inputProps={{ step: 0.1, min: 0, max: 1 }}
                  size="small"
                  sx={{ width: 100 }}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Tab Panel 2: Questions */}
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">Генерация тестовых вопросов</Typography>
                  <Button 
                    variant="contained" 
                    onClick={handleGenerateQuestions}
                    disabled={generatingQuestions}
                  >
                    {generatingQuestions ? 'Генерация...' : 'Сгенерировать вопросы'}
                  </Button>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Вопросы генерируются на основе нормативных документов и промптов
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  База вопросов
                </Typography>
                <Alert severity="info" sx={{ mb: 2 }}>
                  Здесь будет отображаться список всех сгенерированных вопросов с возможностью редактирования
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Tab Panel 3: Cases */}
      <TabPanel value={tabValue} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">Генерация кейсов</Typography>
                  <Button 
                    variant="contained" 
                    onClick={handleGenerateCases}
                    disabled={generatingCases}
                  >
                    {generatingCases ? 'Генерация...' : 'Сгенерировать кейсы'}
                  </Button>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Кейсы генерируются на основе шаблонов и нормативных документов
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  База кейсов
                </Typography>
                <Alert severity="info" sx={{ mb: 2 }}>
                  Здесь будет отображаться список всех сгенерированных кейсов
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Tab Panel 4: Analytics */}
      <TabPanel value={tabValue} index={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="text.secondary">
                  Всего руководителей
                </Typography>
                <Typography variant="h3" align="center">
                  0
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="text.secondary">
                  Пройдено тестирований
                </Typography>
                <Typography variant="h3" align="center">
                  0
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" color="text.secondary">
                  Средний балл
                </Typography>
                <Typography variant="h3" align="center">
                  -
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">Кластеризация руководителей</Typography>
                  <Button 
                    variant="contained" 
                    onClick={handleRunClustering}
                  >
                    Запустить кластеризацию
                  </Button>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  Группировка руководителей по результатам тестирования
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Образовательные программы
                </Typography>
                <Alert severity="info">
                  После кластеризации здесь появятся рекомендации по образовательным программам для каждого кластера
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Tab Panel 5: Schedule */}
      <TabPanel value={tabValue} index={5}>
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Календарь тестирований</Typography>
              <Button variant="contained">
                Запланировать тестирование
              </Button>
            </Box>
            <Alert severity="info">
              Календарь запланированных тестирований для организаций и кандидатов
            </Alert>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Prompt Dialog */}
      <Dialog open={promptDialogOpen} onClose={() => setPromptDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Управление промптами</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Выберите категорию и тип организации для редактирования промпта
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={10}
            placeholder="Текст промпта..."
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPromptDialogOpen(false)}>Отмена</Button>
          <Button variant="contained" onClick={() => setPromptDialogOpen(false)}>
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
