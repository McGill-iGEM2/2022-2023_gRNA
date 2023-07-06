import pandas as pd
import glob

print("Please input the full path (starting from C:/...) of the directory containing all TSVs (subdirectories within the directory is no issue).")
directory_path = input("Use format --C:/Users/steph/Dry Lab TCGA Data/-- if Dry Lab TCGA Data is your directory: ")
all_tsv_files = glob.glob(directory_path + "**/*.tsv", recursive=True)
percentile = float(input("Please input the desired percentile cutoff for considering genes as \'expressed\': "))
super_df = pd.DataFrame({'gene_id':[], 'gene_name':[]})

def sort_tpms(file_name):
    df = pd.read_table(file_name)
    df = df.reset_index()
    new_header = df.iloc[0] 
    df = df[1:]
    df.columns = new_header

    tpm_values = df[['gene_id','gene_name','tpm_unstranded']]
    tpm_values = tpm_values[4:]
    tpm_values = tpm_values.astype({'gene_id':'string', 'gene_name':'string', 'tpm_unstranded':'float'})
    tpm_values = tpm_values.sort_values(by="tpm_unstranded", ascending=False)
    
    return tpm_values

def take_percentile(df):
    num_rows = len(df.index)
    expressed_genes = df.iloc[0:(round((num_rows*percentile)/100))]
    expressed_genes = expressed_genes.reset_index(drop=True)
    return expressed_genes


index = 1
for tsv_file in all_tsv_files:
    print('Progress: '+str(index)+' of 563 files', end="\r")
    tpm_raw = sort_tpms(tsv_file)
    tpms_expressed = take_percentile(tpm_raw)
    expressed_genes = tpms_expressed[['gene_id', 'gene_name']]
    super_df = pd.concat([super_df, expressed_genes], ignore_index=True)
    index += 1

final_df = super_df.pivot_table(index = ['gene_id', 'gene_name'], aggfunc ='size')
final_df = final_df.to_frame()
final_df = final_df.reset_index()
final_df.rename(columns={final_df.columns[2]: 'expressions'},inplace=True)
final_df = final_df.sort_values(by="expressions", ascending=False)
final_df = final_df.reset_index()
final_df['expression_rate'] = (final_df['expressions']/563)*100
final_df['percentile'] = (final_df['expressions'].rank(pct=True))*100
final_df = final_df.reset_index(drop=True)

print(final_df)
final_df.to_csv("tcga_cleaned_data.tsv", sep="\t", index=False)
