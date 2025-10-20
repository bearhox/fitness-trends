import pandas as pd
from collections import Counter
import re

def simple_food_analysis():
    """Simple, robust food log analysis"""
    
    print("=== SIMPLE FOOD LOG ANALYSIS ===\n")
    
    try:
        # Read Excel file
        print("Reading Excel file...")
        df = pd.read_excel('foodlog_2025.xlsx')
        print(f"✅ Successfully loaded {len(df)} rows, {len(df.columns)} columns\n")
        
        # Show basic structure
        print("COLUMN NAMES:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. {col}")
        
        print(f"\nFIRST 3 ROWS:")
        for i in range(min(3, len(df))):
            print(f"\nRow {i+1}:")
            for col in df.columns:
                value = df.iloc[i][col]
                if pd.notna(value):
                    print(f"  {col}: {value}")
        
        # Find all unique text values (potential foods)
        print(f"\n" + "="*50)
        print("EXTRACTING ALL FOODS/TEXT FROM YOUR LOG:")
        print("="*50)
        
        all_text = []
        for col in df.columns:
            for value in df[col]:
                if pd.notna(value) and isinstance(value, str):
                    all_text.append(str(value).lower().strip())
        
        # Split into words and count
        all_words = []
        for text in all_text:
            # Split on common separators
            words = re.split(r'[,;|\n\r\t\-\(\)]+', text)
            for word in words:
                clean_word = word.strip()
                if len(clean_word) > 2 and not clean_word.isdigit():
                    all_words.append(clean_word)
        
        # Count word frequency
        word_counts = Counter(all_words)
        
        print(f"\nMOST COMMON FOODS/ITEMS (Top 30):")
        for word, count in word_counts.most_common(30):
            print(f"  {word} ({count} times)")
        
        # Try to identify periods if there's date info
        print(f"\n" + "="*50)
        print("TIME PERIOD ANALYSIS:")
        print("="*50)
        
        # Look for date columns
        date_columns = []
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                date_columns.append(col)
        
        if date_columns:
            print(f"Found potential date columns: {date_columns}")
            
            for date_col in date_columns:
                print(f"\nAnalyzing column: {date_col}")
                try:
                    df['parsed_date'] = pd.to_datetime(df[date_col], errors='coerce')
                    valid_dates = df['parsed_date'].notna().sum()
                    print(f"  Valid dates found: {valid_dates}")
                    
                    if valid_dates > 0:
                        # Group by month
                        df['month'] = df['parsed_date'].dt.month
                        monthly_counts = df['month'].value_counts().sort_index()
                        
                        print(f"  Entries by month:")
                        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        for month_num, count in monthly_counts.items():
                            if pd.notna(month_num) and 1 <= month_num <= 12:
                                status = ""
                                if month_num <= 6:
                                    status = " (Kazakhstan - good digestion)"
                                elif month_num <= 8:
                                    status = " (Travel - normal)"
                                else:
                                    status = " (US - digestive issues!)"
                                print(f"    {months[int(month_num)-1]}: {count} entries{status}")
                        break
                except:
                    print(f"  Could not parse dates in {date_col}")
        else:
            print("No clear date columns found.")
            print("Assuming chronological order...")
            
            total_rows = len(df)
            if total_rows > 0:
                # Rough periods based on position
                kz_end = total_rows // 2
                us_start = int(total_rows * 0.7)
                
                print(f"  Kazakhstan period (rows 1-{kz_end}): Good digestion")
                print(f"  Travel period (rows {kz_end+1}-{us_start}): Normal digestion")  
                print(f"  US return period (rows {us_start+1}-{total_rows}): DIGESTIVE ISSUES")
        
        # Recommendations
        print(f"\n" + "="*50)
        print("🎯 RECOMMENDATIONS:")
        print("="*50)
        
        print("""
1. LOOK FOR PATTERNS: Review the most common foods above
   - Which ones did you start eating MORE of after returning to US?
   - Which ones are NEW since August 9th?

2. HIGH-RISK ITEMS TO INVESTIGATE:
   - Any restaurant/takeout foods
   - New brands of gluten-free products  
   - Oats (different processing in US)
   - Dairy products (secondary lactose intolerance)
   - Sauces, seasonings, condiments

3. ELIMINATION TRIAL (2 weeks each):
   - Week 1-2: No restaurant food, only home-cooked
   - Week 3-4: No dairy products
   - Week 5-6: Switch ALL gluten-free brands to different ones

4. KEEP TRACKING: Note which days you have worse symptoms
        """)
        
    except FileNotFoundError:
        print("❌ Error: Could not find 'foodlog_2025.xlsx'")
        print("Make sure the file is in the same directory as this script")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTry these troubleshooting steps:")
        print("1. Make sure file is named exactly 'foodlog_2025.xlsx'")
        print("2. Try: pip install --upgrade pandas openpyxl")
        print("3. Check if file is corrupted by opening it in Excel first")

# Run the analysis
if __name__ == "__main__":
    simple_food_analysis()
