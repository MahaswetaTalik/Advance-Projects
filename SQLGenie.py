{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "62760a49-1b73-4b65-8996-0ecb9103d847",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "bf069829-1540-4220-a4e8-ae17df52e8c6",
   "metadata": {},
   "source": [
    "# Load and Preprocess Datasets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "id": "5c4fa9e8-58ef-4b1a-93c5-30d61adff9b5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "nlp_df = pd.read_csv('nl_to_sql_dataset.csv')\n",
    "base_constraints_df = pd.read_csv('sql_constraints_base.csv')\n",
    "strong_constraints_df = pd.read_csv('sql_constraints_strong.csv')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "4ed730bd-d7ab-4906-bfcf-f81638af8b6a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NL → SQL dataset shape: (5, 2)\n",
      "Base constraints shape: (88, 3)\n",
      "Strong constraints shape: (96, 3)\n"
     ]
    }
   ],
   "source": [
    "print(\"NL → SQL dataset shape:\", nlp_df.shape)\n",
    "print(\"Base constraints shape:\", base_constraints_df.shape)\n",
    "print(\"Strong constraints shape:\", strong_constraints_df.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "aa4dbcd1-ab8c-416f-b0fb-664f870a34c2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NL_Query    0\n",
      "SQL         0\n",
      "dtype: int64\n",
      "Constraint_Type     0\n",
      "Description        54\n",
      "Example_SQL        88\n",
      "dtype: int64\n",
      "Constraint_Type     0\n",
      "Description        54\n",
      "Example_SQL        88\n",
      "dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(nlp_df.isna().sum())\n",
    "print(base_constraints_df.isna().sum())\n",
    "print(strong_constraints_df.isna().sum())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "id": "f6d9f859-c275-4138-af8b-9fda19836a03",
   "metadata": {},
   "outputs": [],
   "source": [
    "# function to generate placeholder descriptions\n",
    "def fill_description(row):\n",
    "    if pd.isna(row['Description']):\n",
    "        return f\"{row['Constraint_Type']} constraint description pending.\"\n",
    "    return row['Description']\n",
    "\n",
    "base_constraints_df['Description'] = base_constraints_df.apply(fill_description, axis=1)\n",
    "strong_constraints_df['Description'] = strong_constraints_df.apply(fill_description, axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "id": "aaadf0fb-f76a-4129-9f15-e5820d795738",
   "metadata": {},
   "outputs": [],
   "source": [
    "# function to generate placeholder SQL examples\n",
    "def fill_example_sql(row):\n",
    "    if pd.isna(row['Example_SQL']):\n",
    "        return f\"-- Example SQL for {row['Constraint_Type']} constraint to be added.\"\n",
    "    return row['Example_SQL']\n",
    "\n",
    "base_constraints_df['Example_SQL'] = base_constraints_df.apply(fill_example_sql, axis=1)\n",
    "strong_constraints_df['Example_SQL'] = strong_constraints_df.apply(fill_example_sql, axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "id": "0d8453a0-e393-4546-b380-57ca305cd912",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NL_Query    0\n",
      "SQL         0\n",
      "dtype: int64\n",
      "Constraint_Type    0\n",
      "Description        0\n",
      "Example_SQL        0\n",
      "dtype: int64\n",
      "Constraint_Type    0\n",
      "Description        0\n",
      "Example_SQL        0\n",
      "dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(nlp_df.isna().sum())\n",
    "print(base_constraints_df.isna().sum())\n",
    "print(strong_constraints_df.isna().sum())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "id": "3eba0db9-c4ee-4aa8-9330-298c59931641",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Total constraints after merge: (184, 3)\n"
     ]
    }
   ],
   "source": [
    "# merge constraints\n",
    "\n",
    "constraints_df = pd.concat([base_constraints_df, strong_constraints_df], ignore_index=True)\n",
    "print(\"Total constraints after merge:\", constraints_df.shape)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6d94c211-41d8-42a6-b2a7-ad8e72acda72",
   "metadata": {},
   "source": [
    "# Preprocess NL → SQL Dataset"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "23facf96-6e3b-4f00-9954-0e8b99e6423a",
   "metadata": {},
   "source": [
    "Clean text\n",
    "\n",
    "Lowercase, remove unnecessary spaces\n",
    "\n",
    "Handle missing SQL"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "id": "d2662ace-3ade-49aa-878e-85161e2760b7",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Index(['NL_Query', 'SQL'], dtype='object')\n"
     ]
    }
   ],
   "source": [
    "print(nlp_df.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "id": "a75d1186-b37a-4d0f-a609-0725175a6a4b",
   "metadata": {},
   "outputs": [],
   "source": [
    "nlp_df['NL_Query'] = nlp_df['NL_Query'].str.strip()\n",
    "nlp_df['SQL'] = nlp_df['SQL'].str.strip()\n",
    "nlp_df.dropna(subset=['NL_Query', 'SQL'], inplace=True)\n",
    "\n",
    "# lowercase all\n",
    "nlp_df['NL_Query'] = nlp_df['NL_Query'].str.lower()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "id": "fe04ca49-24c5-480f-bf93-bd4a07d88860",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Master dataset shape: (189, 6)\n",
      "                                            NL_Query  \\\n",
      "0                    get all employees older than 30   \n",
      "1                   list all orders for customer 101   \n",
      "2  show product names with default status 'availa...   \n",
      "3     insert a new student with id 1 and name 'rahi'   \n",
      "4                 delete all orders of customer 9999   \n",
      "\n",
      "                                                 SQL    source  \\\n",
      "0            SELECT * FROM Employees WHERE Age > 30;  nlp_base   \n",
      "1       SELECT * FROM Orders WHERE CustomerID = 101;  nlp_base   \n",
      "2  SELECT ProductID, Status FROM Products WHERE S...  nlp_base   \n",
      "3  INSERT INTO Students (ID, Name) VALUES (1, 'Ra...  nlp_base   \n",
      "4        DELETE FROM Orders WHERE CustomerID = 9999;  nlp_base   \n",
      "\n",
      "  Constraint_Type Description Example_SQL  \n",
      "0             NaN         NaN         NaN  \n",
      "1             NaN         NaN         NaN  \n",
      "2             NaN         NaN         NaN  \n",
      "3             NaN         NaN         NaN  \n",
      "4             NaN         NaN         NaN  \n"
     ]
    }
   ],
   "source": [
    "# Combine all dataset\n",
    "\n",
    "nlp_df['source'] = 'nlp_base'\n",
    "base_constraints_df['source'] = 'constraints_base'\n",
    "strong_constraints_df['source'] = 'constraints_strong'\n",
    "\n",
    "# Combine all\n",
    "master_df = pd.concat([nlp_df, base_constraints_df, strong_constraints_df], ignore_index=True)\n",
    "print(\"Master dataset shape:\", master_df.shape)\n",
    "print(master_df.head())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "id": "c3c173a4-5b92-44ec-9964-427d20a38b9c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "source\n",
      "constraints_strong    96\n",
      "constraints_base      88\n",
      "nlp_base               5\n",
      "Name: count, dtype: int64\n",
      "SQL\n",
      "SELECT    3\n",
      "INSERT    1\n",
      "DELETE    1\n",
      "Name: count, dtype: int64\n"
     ]
    }
   ],
   "source": [
    "# check diversity of the dataset\n",
    "\n",
    "# Count examples per source\n",
    "print(master_df['source'].value_counts())\n",
    "\n",
    "# Optional: check SQL types coverage\n",
    "sql_types = master_df['SQL'].str.extract(r'^(SELECT|INSERT|UPDATE|DELETE)', expand=False)\n",
    "print(sql_types.value_counts())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "a7fbc8ba-7d2d-4a14-bd74-0aac2ee044c4",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "master_df = pd.read_csv(\"master_nlp_sql_dataset.csv\") \n",
    "\n",
    "master_df.dropna(subset=['NL_Query', 'SQL'], inplace=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "id": "da41be9d-8e90-4681-9942-9f5e76eb5e28",
   "metadata": {},
   "outputs": [],
   "source": [
    "master_df['NL_Query'] = master_df['NL_Query'].str.strip().str.lower()\n",
    "master_df['SQL'] = master_df['SQL'].str.strip()\n",
    "\n",
    "# Define X and y\n",
    "X = master_df['NL_Query'].str.lower().tolist() # input: natural language queries\n",
    "y = master_df['SQL'].tolist()  # output: corresponding SQL queries\n",
    "\n",
    "# Create a simple dictionary for fast rule-based lookup\n",
    "nl_to_sql_dict = dict(zip(X, y))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ae681a57-ab3f-498a-a80b-666e1f038a07",
   "metadata": {},
   "source": [
    "# Tokenize and Encode"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 101,
   "id": "705718ce-5ebd-4889-a9c1-3550224c2be4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: transformers==4.40.2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (4.40.2)\n",
      "Requirement already satisfied: filelock in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (3.18.0)\n",
      "Requirement already satisfied: huggingface-hub<1.0,>=0.19.3 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (0.35.3)\n",
      "Requirement already satisfied: numpy>=1.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (2.1.3)\n",
      "Requirement already satisfied: packaging>=20.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (25.0)\n",
      "Requirement already satisfied: pyyaml>=5.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (6.0.2)\n",
      "Requirement already satisfied: regex!=2019.12.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (2024.11.6)\n",
      "Requirement already satisfied: requests in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (2.32.4)\n",
      "Requirement already satisfied: tokenizers<0.20,>=0.19 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (0.19.1)\n",
      "Requirement already satisfied: safetensors>=0.4.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (0.5.3)\n",
      "Requirement already satisfied: tqdm>=4.27 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (4.67.1)\n",
      "Requirement already satisfied: fsspec>=2023.5.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from huggingface-hub<1.0,>=0.19.3->transformers==4.40.2) (2025.3.0)\n",
      "Requirement already satisfied: typing-extensions>=3.7.4.3 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from huggingface-hub<1.0,>=0.19.3->transformers==4.40.2) (4.14.1)\n",
      "Requirement already satisfied: colorama in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from tqdm>=4.27->transformers==4.40.2) (0.4.6)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (3.4.2)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (3.10)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (2.5.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (2025.6.15)\n",
      "Requirement already satisfied: torch in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (2.8.0)\n",
      "Requirement already satisfied: filelock in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from torch) (3.18.0)\n",
      "Requirement already satisfied: typing-extensions>=4.10.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from torch) (4.14.1)\n",
      "Requirement already satisfied: sympy>=1.13.3 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from torch) (1.14.0)\n",
      "Requirement already satisfied: networkx in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from torch) (3.5)\n",
      "Requirement already satisfied: jinja2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from torch) (3.1.6)\n",
      "Requirement already satisfied: fsspec in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from torch) (2025.3.0)\n",
      "Requirement already satisfied: mpmath<1.4,>=1.1.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from sympy>=1.13.3->torch) (1.3.0)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from jinja2->torch) (3.0.2)\n",
      "Requirement already satisfied: datasets in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (4.0.0)\n",
      "Requirement already satisfied: filelock in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (3.18.0)\n",
      "Requirement already satisfied: numpy>=1.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (2.1.3)\n",
      "Requirement already satisfied: pyarrow>=15.0.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (20.0.0)\n",
      "Requirement already satisfied: dill<0.3.9,>=0.3.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (0.3.8)\n",
      "Requirement already satisfied: pandas in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (2.3.0)\n",
      "Requirement already satisfied: requests>=2.32.2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (2.32.4)\n",
      "Requirement already satisfied: tqdm>=4.66.3 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (4.67.1)\n",
      "Requirement already satisfied: xxhash in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (3.5.0)\n",
      "Requirement already satisfied: multiprocess<0.70.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (0.70.16)\n",
      "Requirement already satisfied: fsspec<=2025.3.0,>=2023.1.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (2025.3.0)\n",
      "Requirement already satisfied: huggingface-hub>=0.24.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (0.35.3)\n",
      "Requirement already satisfied: packaging in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (25.0)\n",
      "Requirement already satisfied: pyyaml>=5.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from datasets) (6.0.2)\n",
      "Requirement already satisfied: aiohttp!=4.0.0a0,!=4.0.0a1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (3.12.15)\n",
      "Requirement already satisfied: aiohappyeyeballs>=2.5.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (2.6.1)\n",
      "Requirement already satisfied: aiosignal>=1.4.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (1.4.0)\n",
      "Requirement already satisfied: attrs>=17.3.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (25.3.0)\n",
      "Requirement already satisfied: frozenlist>=1.1.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (1.7.0)\n",
      "Requirement already satisfied: multidict<7.0,>=4.5 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (6.6.3)\n",
      "Requirement already satisfied: propcache>=0.2.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (0.3.2)\n",
      "Requirement already satisfied: yarl<2.0,>=1.17.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (1.20.1)\n",
      "Requirement already satisfied: idna>=2.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from yarl<2.0,>=1.17.0->aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (3.10)\n",
      "Requirement already satisfied: typing-extensions>=4.2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from aiosignal>=1.4.0->aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.3.0,>=2023.1.0->datasets) (4.14.1)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests>=2.32.2->datasets) (3.4.2)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests>=2.32.2->datasets) (2.5.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests>=2.32.2->datasets) (2025.6.15)\n",
      "Requirement already satisfied: colorama in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from tqdm>=4.66.3->datasets) (0.4.6)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from pandas->datasets) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from pandas->datasets) (2025.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from pandas->datasets) (2025.2)\n",
      "Requirement already satisfied: six>=1.5 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from python-dateutil>=2.8.2->pandas->datasets) (1.17.0)\n"
     ]
    }
   ],
   "source": [
    "!pip install transformers==4.40.2\n",
    "!pip install torch --upgrade\n",
    "!pip install datasets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 102,
   "id": "9c1249aa-6a3e-4825-b7e3-5a74d671720d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Imports successful!\n"
     ]
    }
   ],
   "source": [
    "from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq\n",
    "print(\"Imports successful!\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 103,
   "id": "56188be1-7d93-4acb-ac26-5c8c42fe9002",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: sentencepiece in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (0.2.1)\n"
     ]
    }
   ],
   "source": [
    "!pip install sentencepiece"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 104,
   "id": "6e1231e8-6b6b-43c7-8c3a-02ec5eb76b8e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "SentencePiece installed successfully!\n"
     ]
    }
   ],
   "source": [
    "import sentencepiece\n",
    "print(\"SentencePiece installed successfully!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "34171fa4-3e7b-442a-80b4-8d7b44f1042b",
   "metadata": {},
   "source": [
    "# Prepare Dataset for T5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 105,
   "id": "d580dab0-ced2-4002-b4a9-4c80b9045c61",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Training examples: 4\n",
      "Testing examples: 1\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "# Load your master dataset\n",
    "master_df = pd.read_csv(\"master_nlp_sql_dataset.csv\")  # your combined dataset\n",
    "master_df.dropna(subset=['NL_Query', 'SQL'], inplace=True)\n",
    "\n",
    "# Optional: lowercase everything for consistency\n",
    "master_df['NL_Query'] = master_df['NL_Query'].str.lower()\n",
    "master_df['SQL'] = master_df['SQL'].str.lower()\n",
    "\n",
    "# Split into train and test\n",
    "train_df, test_df = train_test_split(master_df, test_size=0.1, random_state=42)\n",
    "\n",
    "print(\"Training examples:\", len(train_df))\n",
    "print(\"Testing examples:\", len(test_df))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "338ce8ff-550a-4f83-ad84-607305654fa2",
   "metadata": {},
   "source": [
    "# Create a PyTorch Dataset Class"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 106,
   "id": "be53427a-7df1-45d1-9966-8eaf951169ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "from torch.utils.data import Dataset\n",
    "\n",
    "class SQLDataset(Dataset):\n",
    "    def __init__(self, df, tokenizer, max_len=128):\n",
    "        self.df = df\n",
    "        self.tokenizer = tokenizer\n",
    "        self.max_len = max_len\n",
    "\n",
    "    def __len__(self):\n",
    "        return len(self.df)\n",
    "\n",
    "    def __getitem__(self, idx):\n",
    "        nl_query = str(self.df.iloc[idx]['NL_Query'])\n",
    "        sql_query = str(self.df.iloc[idx]['SQL'])\n",
    "\n",
    "        input_encoding = self.tokenizer(\n",
    "            nl_query,\n",
    "            max_length=self.max_len,\n",
    "            padding='max_length',\n",
    "            truncation=True,\n",
    "            return_tensors=\"pt\"\n",
    "        )\n",
    "        target_encoding = self.tokenizer(\n",
    "            sql_query,\n",
    "            max_length=self.max_len,\n",
    "            padding='max_length',\n",
    "            truncation=True,\n",
    "            return_tensors=\"pt\"\n",
    "        )\n",
    "\n",
    "        return {\n",
    "            \"input_ids\": input_encoding['input_ids'].squeeze(),\n",
    "            \"attention_mask\": input_encoding['attention_mask'].squeeze(),\n",
    "            \"labels\": target_encoding['input_ids'].squeeze()\n",
    "        }\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 107,
   "id": "b9f98df9-acd7-4ff6-8e1d-d4015ab6ba83",
   "metadata": {},
   "outputs": [],
   "source": [
    "train_dataset = SQLDataset(train_df, tokenizer)\n",
    "test_dataset = SQLDataset(test_df, tokenizer)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 108,
   "id": "4355e563-c0cb-4d64-8379-12c9ef36aec0",
   "metadata": {},
   "outputs": [],
   "source": [
    "from torch.utils.data import DataLoader\n",
    "\n",
    "train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)\n",
    "test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "122eaed8-bced-46ad-9b22-d3e53863bfd3",
   "metadata": {},
   "source": [
    "# Initialize Tokenizer and Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 109,
   "id": "23b97724-2aa0-4449-8c1a-c3bae883df65",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\KIIT0001\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\huggingface_hub\\file_download.py:945: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.\n",
      "  warnings.warn(\n",
      "Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.\n"
     ]
    }
   ],
   "source": [
    "from transformers import T5Tokenizer, T5ForConditionalGeneration\n",
    "\n",
    "model_name = \"t5-small\"  # lightweight, works locally\n",
    "tokenizer = T5Tokenizer.from_pretrained(model_name)\n",
    "model = T5ForConditionalGeneration.from_pretrained(model_name)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 110,
   "id": "7396a895-5b4b-4ef1-91f6-34b8a1085680",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\KIIT0001\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\transformers\\optimization.py:521: FutureWarning: This implementation of AdamW is deprecated and will be removed in a future version. Use the PyTorch implementation torch.optim.AdamW instead, or set `no_deprecation_warning=True` to disable this warning\n",
      "  warnings.warn(\n"
     ]
    }
   ],
   "source": [
    "import torch\n",
    "from transformers import T5ForConditionalGeneration, AdamW\n",
    "\n",
    "device = torch.device(\"cuda\" if torch.cuda.is_available() else \"cpu\")\n",
    "\n",
    "model = T5ForConditionalGeneration.from_pretrained(\"t5-small\")\n",
    "model.to(device)\n",
    "\n",
    "optimizer = AdamW(model.parameters(), lr=5e-5)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 111,
   "id": "953cd354-fda4-4406-b162-1226e04c73c8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/3\n",
      "Average Loss: 14.9695\n",
      "Epoch 2/3\n",
      "Average Loss: 13.9400\n",
      "Epoch 3/3\n",
      "Average Loss: 12.5780\n"
     ]
    }
   ],
   "source": [
    "epochs = 3  # you can increase later\n",
    "\n",
    "model.train()\n",
    "for epoch in range(epochs):\n",
    "    print(f\"Epoch {epoch+1}/{epochs}\")\n",
    "    total_loss = 0\n",
    "    for batch in train_loader:\n",
    "        optimizer.zero_grad()\n",
    "        \n",
    "        input_ids = batch[\"input_ids\"].to(device)\n",
    "        attention_mask = batch[\"attention_mask\"].to(device)\n",
    "        labels = batch[\"labels\"].to(device)\n",
    "\n",
    "        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)\n",
    "        loss = outputs.loss\n",
    "        loss.backward()\n",
    "        optimizer.step()\n",
    "\n",
    "        total_loss += loss.item()\n",
    "    \n",
    "    print(f\"Average Loss: {total_loss / len(train_loader):.4f}\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b3d5b58b-18e4-49c7-b60e-354e4c523fe0",
   "metadata": {},
   "source": [
    "# Evaluate and Test "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 115,
   "id": "4b4a2c82-7bcd-4ed3-8638-1c2e13a85439",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Found existing installation: transformers 4.33.0\n",
      "Uninstalling transformers-4.33.0:\n",
      "  Successfully uninstalled transformers-4.33.0\n"
     ]
    }
   ],
   "source": [
    "!pip uninstall -y transformers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 117,
   "id": "f324d251-bc2c-4756-a996-de477356624f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: transformers==4.40.2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (4.40.2)\n",
      "Requirement already satisfied: filelock in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (3.18.0)\n",
      "Requirement already satisfied: huggingface-hub<1.0,>=0.19.3 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (0.35.3)\n",
      "Requirement already satisfied: numpy>=1.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (2.1.3)\n",
      "Requirement already satisfied: packaging>=20.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (25.0)\n",
      "Requirement already satisfied: pyyaml>=5.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (6.0.2)\n",
      "Requirement already satisfied: regex!=2019.12.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (2024.11.6)\n",
      "Requirement already satisfied: requests in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (2.32.4)\n",
      "Requirement already satisfied: tokenizers<0.20,>=0.19 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (0.19.1)\n",
      "Requirement already satisfied: safetensors>=0.4.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (0.5.3)\n",
      "Requirement already satisfied: tqdm>=4.27 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from transformers==4.40.2) (4.67.1)\n",
      "Requirement already satisfied: fsspec>=2023.5.0 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from huggingface-hub<1.0,>=0.19.3->transformers==4.40.2) (2025.3.0)\n",
      "Requirement already satisfied: typing-extensions>=3.7.4.3 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from huggingface-hub<1.0,>=0.19.3->transformers==4.40.2) (4.14.1)\n",
      "Requirement already satisfied: colorama in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from tqdm>=4.27->transformers==4.40.2) (0.4.6)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (3.4.2)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (3.10)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (2.5.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\users\\kiit0001\\appdata\\local\\programs\\python\\python311\\lib\\site-packages (from requests->transformers==4.40.2) (2025.6.15)\n"
     ]
    }
   ],
   "source": [
    "!pip install transformers==4.40.2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 118,
   "id": "616f1a3f-8dc5-4f0c-b1e6-652dd63489dc",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NL Query: Get all employees where age > 30\n",
      "SQL Query: erg get a job job : og get a job where ages > 30 years\n"
     ]
    }
   ],
   "source": [
    "def predict_sql(query):\n",
    "    inputs = tokenizer(query.lower(), return_tensors=\"pt\", padding=True, truncation=True)\n",
    "    outputs = model.generate(**inputs, max_length=128)\n",
    "    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)\n",
    "    return sql\n",
    "\n",
    "# Example\n",
    "test_query = \"Get all employees where age > 30\"\n",
    "print(\"NL Query:\", test_query)\n",
    "print(\"SQL Query:\", predict_sql(test_query))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0d8e75d0-9c22-4a30-9e9a-aa443cccf2af",
   "metadata": {},
   "source": [
    "# Save and Load Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 125,
   "id": "f2ca13c1-b05d-4dda-a25e-e2c31d35485d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model and tokenizer saved successfully!\n"
     ]
    }
   ],
   "source": [
    "# Save model and tokenizer safely\n",
    "model.save_pretrained(\"./sqlgenie_t5_model\")\n",
    "tokenizer.save_pretrained(\"./sqlgenie_t5_model\")\n",
    "\n",
    "print(\"Model and tokenizer saved successfully!\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 126,
   "id": "f56d76e8-3456-482b-8806-66074429d6ab",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "✅ Model loaded successfully!\n"
     ]
    }
   ],
   "source": [
    "from transformers import T5Tokenizer, T5ForConditionalGeneration\n",
    "import torch\n",
    "\n",
    "#  Load the saved model and tokenizer\n",
    "model_path = \"./sqlgenie_t5_model\"\n",
    "\n",
    "tokenizer = T5Tokenizer.from_pretrained(model_path)\n",
    "model = T5ForConditionalGeneration.from_pretrained(model_path)\n",
    "\n",
    "device = torch.device(\"cuda\" if torch.cuda.is_available() else \"cpu\")\n",
    "model.to(device)\n",
    "\n",
    "print(\"✅ Model loaded successfully!\")\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "997e5e5a-31ef-4ba6-9d5a-209d607ee460",
   "metadata": {},
   "source": [
    "# Rule-based Fallback"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 128,
   "id": "0a459594-9646-4394-a4b9-e29a733605e5",
   "metadata": {},
   "outputs": [],
   "source": [
    "def sqlgenie_predict(nl_query):\n",
    "    # 1. Try ML model\n",
    "    try:\n",
    "        sql = predict_sql(nl_query)\n",
    "        if sql.strip() != \"\":\n",
    "            return sql\n",
    "    except:\n",
    "        pass\n",
    "    # 2. Fallback to rule-based converter\n",
    "    return convert_to_sql_advanced(nl_query)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "668e2594-8fc7-4ebf-80a2-43a94af620c8",
   "metadata": {},
   "source": [
    "# Testing on batch queries "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 129,
   "id": "c1b5bce5-ae16-4ee7-8f70-c1e7d84773bc",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NL Query: Get all employees\n",
      "SQL Query: Get to all employees\n",
      "--------------------------------------------------\n",
      "NL Query: Show employees where age is null\n",
      "SQL Query: Show employees where age is null\n",
      "--------------------------------------------------\n",
      "NL Query: List unique customer names\n",
      "SQL Query: List unique customer names\n",
      "--------------------------------------------------\n",
      "NL Query: Find orders where amount > 5000\n",
      "SQL Query: Find orders where amount > 5000\n",
      "--------------------------------------------------\n"
     ]
    }
   ],
   "source": [
    "test_queries = [\n",
    "    \"Get all employees\",\n",
    "    \"Show employees where age is null\",\n",
    "    \"List unique customer names\",\n",
    "    \"Find orders where amount > 5000\"\n",
    "]\n",
    "\n",
    "for q in test_queries:\n",
    "    print(\"NL Query:\", q)\n",
    "    print(\"SQL Query:\", sqlgenie_predict(q))\n",
    "    print(\"-\"*50)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "15e39b11-0b8c-4f96-81e5-16b894edee17",
   "metadata": {},
   "source": [
    "# Some changes for UI things"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "60e757d2-b6eb-48db-afb4-38ffa9c1de1a",
   "metadata": {},
   "source": [
    "Making a overall convert function which will have all the possible cases and conditions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 147,
   "id": "24ecc18b-f2b9-4871-8faf-b5e4d77dca68",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "master_df = pd.read_csv(\"master_nlp_sql_dataset.csv\")\n",
    "master_df['NL_Query'] = master_df['NL_Query'].astype(str).str.strip().str.lower()\n",
    "master_df['SQL'] = master_df['SQL'].astype(str).str.strip()\n",
    "\n",
    "\n",
    "def replace_with_constraints(col):\n",
    "    return col.strip()\n",
    "\n",
    "def infer_table(col):\n",
    "   \n",
    "    table_mapping = {\n",
    "        \"name\": \"Customers\",\n",
    "        \"customer_id\": \"Customers\",\n",
    "        \"country\": \"Customers\",\n",
    "        \"order_id\": \"Orders\",\n",
    "        \"amount\": \"Orders\",\n",
    "        \"status\": \"Orders\",\n",
    "        \"employee_id\": \"Employees\",\n",
    "        \"age\": \"Employees\",\n",
    "        \"salary\": \"Employees\",\n",
    "        \"date\": \"Orders\"\n",
    "    }\n",
    "    return table_mapping.get(col.lower(), \"UnknownTable\")\n",
    "\n",
    "def handle_basic_match(nl_query):\n",
    "    for _, row in master_df.iterrows():\n",
    "        nl_text = str(row['NL_Query'])\n",
    "        if nl_text and nl_text in nl_query:\n",
    "            sql = str(row['SQL'])\n",
    "            placeholders = re.findall(r\"\\{(\\w+)\\}\", sql)\n",
    "            for ph in placeholders:\n",
    "                sql = sql.replace(f\"{{{ph}}}\", ph)\n",
    "            return sql\n",
    "    return None\n",
    "\n",
    "def handle_nulls(nl_query):\n",
    "    match = re.search(r\"where (\\w+) is (not )?null\", nl_query)\n",
    "    if match:\n",
    "        col, neg = match.groups()\n",
    "        col = replace_with_constraints(col)\n",
    "        condition = \"IS NOT NULL\" if neg else \"IS NULL\"\n",
    "        return f\"SELECT * FROM {infer_table(col)} WHERE {col} {condition};\"\n",
    "    return None\n",
    "\n",
    "def handle_duplicates(nl_query):\n",
    "    if \"distinct\" in nl_query or \"unique\" in nl_query:\n",
    "        match = re.search(r\"(?:distinct|unique) (\\w+)\", nl_query)\n",
    "        if match:\n",
    "            col = replace_with_constraints(match.group(1))\n",
    "            table = infer_table(col)\n",
    "            return f\"SELECT DISTINCT {col} FROM {table};\"\n",
    "    return None\n",
    "\n",
    "def handle_comparisons(nl_query):\n",
    "    match = re.search(r\"where (\\w+) (\\>=|\\<=|!=|=|>|<) (\\w+|\\d+)\", nl_query)\n",
    "    if match:\n",
    "        col, op, val = match.groups()\n",
    "        col = replace_with_constraints(col)\n",
    "        table = infer_table(col)\n",
    "        return f\"SELECT * FROM {table} WHERE {col} {op} {val};\"\n",
    "    return None\n",
    "\n",
    "def handle_aggregation(nl_query):\n",
    "    match = re.search(r\"(count|sum|avg|min|max) (\\w+)\", nl_query)\n",
    "    if match:\n",
    "        func, col = match.groups()\n",
    "        col = replace_with_constraints(col)\n",
    "        table = infer_table(col)\n",
    "        return f\"SELECT {func.upper()}({col}) FROM {table};\"\n",
    "    return None\n",
    "\n",
    "def handle_order_group_limit(nl_query):\n",
    "    sql = None\n",
    "    order_match = re.search(r\"order by (\\w+) (asc|desc)?\", nl_query)\n",
    "    group_match = re.search(r\"group by (\\w+)\", nl_query)\n",
    "    limit_match = re.search(r\"limit (\\d+)\", nl_query)\n",
    "    having_match = re.search(r\"having (.+)\", nl_query)\n",
    "    \n",
    "    table = \"UnknownTable\"\n",
    "    if order_match:\n",
    "        col, direction = order_match.groups()\n",
    "        col = replace_with_constraints(col)\n",
    "        table = infer_table(col)\n",
    "        sql = f\"SELECT * FROM {table} ORDER BY {col} {direction.upper() if direction else 'ASC'};\"\n",
    "    if group_match:\n",
    "        col = replace_with_constraints(group_match.group(1))\n",
    "        table = infer_table(col)\n",
    "        sql = f\"SELECT {col}, COUNT(*) FROM {table} GROUP BY {col}\"\n",
    "        if having_match:\n",
    "            sql += f\" HAVING {having_match.group(1)}\"\n",
    "        sql += \";\"\n",
    "    if limit_match:\n",
    "        limit = int(limit_match.group(1))\n",
    "        sql = f\"SELECT * FROM {table} LIMIT {limit};\"\n",
    "    return sql\n",
    "\n",
    "def handle_joins(nl_query):\n",
    "    match = re.findall(r\"(inner|left|right)?\\s*join (\\w+) on (\\w+)=(\\w+)\", nl_query)\n",
    "    if match:\n",
    "        sql = \"SELECT * FROM \"\n",
    "        tables_used = []\n",
    "        joins = []\n",
    "        for join in match:\n",
    "            join_type, table2, col1, col2 = join\n",
    "            join_type = join_type.upper() if join_type else \"INNER\"\n",
    "            table1 = infer_table(col1)\n",
    "            tables_used.append(table1)\n",
    "            tables_used.append(table2)\n",
    "            joins.append(f\"{join_type} JOIN {table2} ON {table1}.{col1}={table2}.{col2}\")\n",
    "        sql += tables_used[0] + \" \" + \" \".join(joins) + \";\"\n",
    "        return sql\n",
    "    return None\n",
    "\n",
    "def handle_nested_queries(nl_query):\n",
    "    match = re.search(r\"where (\\w+) in \\(select (\\w+) from (\\w+)\\)\", nl_query)\n",
    "    if match:\n",
    "        col_outer, col_inner, table_inner = match.groups()\n",
    "        table_outer = infer_table(col_outer)\n",
    "        return f\"SELECT * FROM {table_outer} WHERE {col_outer} IN (SELECT {col_inner} FROM {table_inner});\"\n",
    "    return None\n",
    "\n",
    "def handle_case_coalesce(nl_query):\n",
    "    match = re.search(r\"case when (.+) then (.+) else (.+) end as (\\w+)\", nl_query)\n",
    "    if match:\n",
    "        cond, val_true, val_false, alias = match.groups()\n",
    "        table = \"UnknownTable\"\n",
    "        return f\"SELECT CASE WHEN {cond} THEN {val_true} ELSE {val_false} END AS {alias} FROM {table};\"\n",
    "    return None\n",
    "\n",
    "def handle_insert_update_delete(nl_query):\n",
    "    if \"insert into\" in nl_query:\n",
    "        match = re.search(r\"insert into (\\w+) \\((.+)\\) values \\((.+)\\)\", nl_query)\n",
    "        if match:\n",
    "            table, cols, vals = match.groups()\n",
    "            return f\"INSERT INTO {table} ({cols}) VALUES ({vals});\"\n",
    "    elif \"update\" in nl_query:\n",
    "        match = re.search(r\"update (\\w+) set (.+) where (.+)\", nl_query)\n",
    "        if match:\n",
    "            table, set_clause, where_clause = match.groups()\n",
    "            return f\"UPDATE {table} SET {set_clause} WHERE {where_clause};\"\n",
    "    elif \"delete from\" in nl_query:\n",
    "        match = re.search(r\"delete from (\\w+) where (.+)\", nl_query)\n",
    "        if match:\n",
    "            table, where_clause = match.groups()\n",
    "            return f\"DELETE FROM {table} WHERE {where_clause};\"\n",
    "    return None\n",
    "\n",
    "def handle_aliasing(nl_query):\n",
    "    match = re.search(r\"select (\\w+) as (\\w+)\", nl_query)\n",
    "    if match:\n",
    "        col, alias = match.groups()\n",
    "        table = infer_table(col)\n",
    "        return f\"SELECT {col} AS {alias} FROM {table};\"\n",
    "    return None\n",
    "\n",
    "def handle_date_filters(nl_query):\n",
    "    if \"last week\" in nl_query:\n",
    "        table = \"Orders\"\n",
    "        return f\"SELECT * FROM {table} WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK);\"\n",
    "    return None\n",
    "\n",
    "def handle_boolean_logic(nl_query):\n",
    "    if \"or\" in nl_query or \"and\" in nl_query or \"not\" in nl_query:\n",
    "        table = \"UnknownTable\"\n",
    "        condition = nl_query.replace(\"who\", \"\").replace(\"bought\", \"\").strip()\n",
    "        condition = re.sub(r\"\\s+\", \" \", condition)\n",
    "        return f\"SELECT * FROM {table} WHERE {condition};\"\n",
    "    return None\n",
    "\n",
    "def handle_table_disambiguation(nl_query):\n",
    "    # Pick first inferred table if multiple match\n",
    "    cols = re.findall(r\"\\w+\", nl_query)\n",
    "    for col in cols:\n",
    "        table = infer_table(col)\n",
    "        if table != \"UnknownTable\":\n",
    "            return f\"SELECT * FROM {table};\"\n",
    "    return None\n",
    "\n",
    "def handle_schema_inference(nl_query):\n",
    "    for col in infer_table.__defaults__[0] if hasattr(infer_table,'__defaults__') else []:\n",
    "        if col in nl_query:\n",
    "            table = infer_table(col)\n",
    "            return f\"SELECT {col} FROM {table};\"\n",
    "    return None\n",
    "\n",
    "def convert_to_sql_master(nl_query):\n",
    "    nl_query_proc = nl_query.strip().lower()\n",
    "    \n",
    "    handlers = [\n",
    "        handle_basic_match,\n",
    "        handle_nulls,\n",
    "        handle_duplicates,\n",
    "        handle_comparisons,\n",
    "        handle_aggregation,\n",
    "        handle_order_group_limit,\n",
    "        handle_joins,\n",
    "        handle_nested_queries,\n",
    "        handle_case_coalesce,\n",
    "        handle_insert_update_delete,\n",
    "        handle_aliasing,\n",
    "        handle_date_filters,\n",
    "        handle_boolean_logic,\n",
    "        handle_table_disambiguation,\n",
    "        handle_schema_inference\n",
    "    ]\n",
    "    \n",
    "    for handler in handlers:\n",
    "        sql = handler(nl_query_proc)\n",
    "        if sql:\n",
    "            return sql\n",
    "    \n",
    "    return \"❌ Sorry! No matching SQL found. Try rephrasing your query.\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 148,
   "id": "74a28945-b49a-4e08-af23-a56edac5ba01",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NL Query: show employees where age is null\n",
      "SQL Query: SELECT * FROM Employees WHERE age IS NULL;\n",
      "--------------------------------------------------\n",
      "NL Query: list unique customer names\n",
      "SQL Query: SELECT DISTINCT customer FROM UnknownTable;\n",
      "--------------------------------------------------\n",
      "NL Query: count orders\n",
      "SQL Query: SELECT COUNT(orders) FROM UnknownTable;\n",
      "--------------------------------------------------\n",
      "NL Query: sum amount from orders\n",
      "SQL Query: SELECT SUM(amount) FROM Orders;\n",
      "--------------------------------------------------\n",
      "NL Query: show orders inner join customers on customer_id=customer_id\n",
      "SQL Query: SELECT * FROM Customers INNER JOIN customers ON Customers.customer_id=customers.customer_id;\n",
      "--------------------------------------------------\n",
      "NL Query: group by country\n",
      "SQL Query: SELECT country, COUNT(*) FROM Customers GROUP BY country;\n",
      "--------------------------------------------------\n",
      "NL Query: order by amount desc\n",
      "SQL Query: SELECT * FROM Orders ORDER BY amount DESC;\n",
      "--------------------------------------------------\n",
      "NL Query: limit 10\n",
      "SQL Query: SELECT * FROM UnknownTable LIMIT 10;\n",
      "--------------------------------------------------\n",
      "NL Query: where employee_id in (select employee_id from employees)\n",
      "SQL Query: SELECT * FROM Employees WHERE employee_id IN (SELECT employee_id FROM employees);\n",
      "--------------------------------------------------\n",
      "NL Query: case when age>30 then 'Senior' else 'Junior' end as level\n",
      "SQL Query: SELECT CASE WHEN age>30 THEN 'senior' ELSE 'junior' END AS level FROM UnknownTable;\n",
      "--------------------------------------------------\n",
      "NL Query: insert into Employees (name, age, salary) values ('John', 30, 5000)\n",
      "SQL Query: INSERT INTO employees (name, age, salary) VALUES ('john', 30, 5000);\n",
      "--------------------------------------------------\n",
      "NL Query: update Employees set salary=6000 where name='John'\n",
      "SQL Query: UPDATE employees SET salary=6000 WHERE name='john';\n",
      "--------------------------------------------------\n",
      "NL Query: delete from Employees where age<25\n",
      "SQL Query: DELETE FROM employees WHERE age<25;\n",
      "--------------------------------------------------\n"
     ]
    }
   ],
   "source": [
    "test_queries = [\n",
    "    \"show employees where age is null\",\n",
    "    \"list unique customer names\",\n",
    "    \"count orders\",\n",
    "    \"sum amount from orders\",\n",
    "    \"show orders inner join customers on customer_id=customer_id\",\n",
    "    \"group by country\",\n",
    "    \"order by amount desc\",\n",
    "    \"limit 10\",\n",
    "    \"where employee_id in (select employee_id from employees)\",\n",
    "    \"case when age>30 then 'Senior' else 'Junior' end as level\",\n",
    "    \"insert into Employees (name, age, salary) values ('John', 30, 5000)\",\n",
    "    \"update Employees set salary=6000 where name='John'\",\n",
    "    \"delete from Employees where age<25\"\n",
    "]\n",
    "\n",
    "for q in test_queries:\n",
    "    print(\"NL Query:\", q)\n",
    "    print(\"SQL Query:\", convert_to_sql_master(q))\n",
    "    print(\"-\"*50)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "58968738-ab0a-4e0e-b5e2-0d958ce20def",
   "metadata": {},
   "source": [
    "# UI Part"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 160,
   "id": "f3d70f20-1569-42ae-95a6-e2ed802c0157",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "* Running on local URL:  http://127.0.0.1:7873\n",
      "* To create a public link, set `share=True` in `launch()`.\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div><iframe src=\"http://127.0.0.1:7873/\" width=\"100%\" height=\"500\" allow=\"autoplay; camera; microphone; clipboard-read; clipboard-write;\" frameborder=\"0\" allowfullscreen></iframe></div>"
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": []
     },
     "execution_count": 160,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import gradio as gr\n",
    "\n",
    "def sqlgenie_ui(nl_query):\n",
    "    sql_query = convert_to_sql_master(nl_query)\n",
    "    return f\"<pre style='background-color:rgba(255,255,255,0.85); color:#000080; padding:15px; border-radius:10px; font-size:14px;'>{sql_query}</pre>\"\n",
    "\n",
    "with gr.Blocks(css=\"\"\"\n",
    "    body, html, .gradio-container {\n",
    "        height: 100% !important;\n",
    "        margin: 0;\n",
    "        padding: 0;\n",
    "        font-family: 'Comic Sans MS', cursive;\n",
    "        background: linear-gradient(135deg, #ffcc33, #ff6666, #33ccff, #33ff77) !important;\n",
    "        background-size: 400% 400% !important;\n",
    "        animation: gradientBG 15s ease infinite !important;\n",
    "    }\n",
    "\n",
    "    @keyframes gradientBG {\n",
    "        0% {background-position:0% 50%;}\n",
    "        50% {background-position:100% 50%;}\n",
    "        100% {background-position:0% 50%;}\n",
    "    }\n",
    "\n",
    "    .gr-block {\n",
    "        background: transparent !important;\n",
    "    }\n",
    "\n",
    "    .gr-button { \n",
    "        background-color: #FFD700 !important; \n",
    "        color: #000 !important; \n",
    "        font-weight: bold !important;\n",
    "        border-radius: 12px !important; \n",
    "        font-size: 16px !important;\n",
    "    }\n",
    "\n",
    "    .gr-textbox textarea { \n",
    "        background-color: rgba(255,255,255,0.9) !important; \n",
    "        color: #000080 !important; \n",
    "        font-size: 14px; \n",
    "        border-radius: 10px; \n",
    "    }\n",
    "\"\"\") as demo:\n",
    "\n",
    "    gr.HTML(\"\"\"\n",
    "    <div style=\"text-align:center; margin-bottom:20px;\">\n",
    "        <h1 style=\"color:#ff0066; text-shadow:2px 2px #ffffff;\">SQLGenie 🧞‍♂️</h1>\n",
    "        <p style=\"color:#000080; font-size:16px;\">Enter your natural language query and get SQL magic instantly! </p>\n",
    "    </div>\n",
    "    \"\"\")\n",
    "\n",
    "    nl_input = gr.Textbox(\n",
    "        label=\"Natural Language Query\",\n",
    "        placeholder=\"e.g., Get all customers who bought product X last week\",\n",
    "        lines=4\n",
    "    )\n",
    "\n",
    "    convert_btn = gr.Button(\"✨ Convert to SQL ✨\")\n",
    "    sql_output = gr.HTML()\n",
    "\n",
    "    convert_btn.click(fn=sqlgenie_ui, inputs=nl_input, outputs=sql_output)\n",
    "\n",
    "demo.launch(share=False, inline=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d1d2bb74-5027-4b46-8f10-33655671c198",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
