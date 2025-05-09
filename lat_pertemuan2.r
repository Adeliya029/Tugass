library(dplyr)
library(tidyr)
library(ggplot2)
library(stringr)

# Data score test by School in NY

SAT.score <- read.csv("C:\\Users\\KPU\\Documents\\Adel\\Saind Data 2024\\smt 2\\MVD\\scores.csv")
head(SAT.score)
view(SAT.score)
set.seed(5293)

# Bersihkan dan pilih data yang relevan
df <- SAT.score %>% 
  filter(!is.na(Average.Score..SAT.Math.)) %>%    
  sample_n(20) %>%    
  rename(Reading = Average.Score..SAT.Reading., 
         Math = Average.Score..SAT.Math.,        
         Writing = Average.Score..SAT.Writing.) %>%
  gather(key = "Test", value = "Mean", "Reading", "Math", "Writing")

top5_city <- SAT.score %>%
  group_by(City) %>%
  slice_max(order_by = Percent.Tested, n = 5, with_ties = FALSE) %>% 
  ungroup()


top5_city %>% print(n = Inf)
view(top5_city)


df_stacked <- top5_city %>%
  select(School.Name, City,
         Math = Average.Score..SAT.Math.,
         Reading = Average.Score..SAT.Reading.,
         Writing = Average.Score..SAT.Writing.) %>%
  pivot_longer(cols = c(Math, Reading, Writing), names_to = "Test", values_to = "Score")

# Visualisasi: Dot chart untuk skor SAT
ggplot(df, aes(x = Mean, y = School.Name, color = Test)) +
  geom_point(size = 3) +
  labs(
    title = "Schools are sorted alphabetically",
    subtitle = "Not the best option",  # sesuai caption gambar
    x = "Mean",
    y = "School Name",
    color = "Test"
  ) +
  theme_minimal(base_size = 12)


ggplot(df, aes(x = reorder(School.Name, Mean), y = Mean, fill = Test)) +
  geom_bar(stat = "identity", position = "dodge") +
  coord_flip() +
  labs(
    title = "Grouped Bar Chart of SAT Scores by Test",
    x = "School Name",
    y = "Mean SAT Score",
    fill = "Test"
  ) +
  theme_minimal(base_size = 12)

ggplot(df, aes(x = reorder(School.Name, Mean), y = Mean, fill = Test)) +
  geom_bar(stat = "identity", position = "stack") +
  coord_flip() +
  labs(
    title = "Stacked Bar Chart of SAT Scores",
    x = "School Name",
    y = "Total SAT Score (stacked)",
    fill = "Test"
  ) +
  theme_minimal(base_size = 12)

df %>% 
  filter(Test == "Math") %>%
  ggplot(aes(x = reorder(School.Name, Mean), y = Mean)) +
  geom_bar(stat = "identity", fill = "#0072B2") +
  coord_flip() +
  labs(
    title = "Bar Chart of Math SAT Scores",
    x = "School Name",
    y = "Math Score"
  ) +
  theme_minimal(base_size = 12)
