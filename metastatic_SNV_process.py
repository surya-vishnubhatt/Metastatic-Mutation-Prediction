import os
import pysam
from collections import defaultdict
import json
import pandas as pd


# Read the Metadata File, Identify Paths for Metadata and Base for Colorectal Metastatic Data
metadata_path = "/athena/khuranalab/scratch/spv4002/Hartwig/metadata.tsv"
metadata = pd.read_csv(metadata_path, sep='\t')
base_dir = "/athena/khuranalab/scratch/spv4002/Hartwig/colorectal_somatic/"

# List the Folder Names (SampleIds)
sample_ids = [name for name in os.listdir('/athena/khuranalab/scratch/spv4002/Hartwig/colorectal_somatic') if os.path.isdir(os.path.join('/athena/khuranalab/scratch/spv4002/Hartwig/colorectal_somatic', name))]

# Extract HmfPatientId for each SampleId
sample_to_patient = metadata[metadata['sampleId'].isin(sample_ids)][['sampleId', 'hmfPatientId']]

# Aggregate SampleIds by HmfPatientId
patient_to_samples = sample_to_patient.groupby('hmfPatientId')['sampleId'].apply(list).to_dict()

#  Report Counts
total_sample_ids = len(sample_ids)
total_patient_ids = len(patient_to_samples.keys())

print(f"Total SampleIds: {total_sample_ids}")
print(f"Total PatientIds: {total_patient_ids}")
print(f"Mapping of PatientIds to SampleIds: {patient_to_samples}")

# Initialize for Further Processing
window_size = 1000000  # 1 Mb
patient_window_mutations = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
total_patients = 728  # Total number of patients

# patient_to_samples is a dictionary mapping patient IDs to lists of sample IDs
# For each patient ID with multiple sample IDs
for patient_id, sample_ids in patient_to_samples.items():
    for sample_id in sample_ids:
        vcf_file_path = os.path.join(base_dir, sample_id, "purple", f"{sample_id}.purple.somatic.vcf.gz")
        if os.path.exists(vcf_file_path):
            vcf_reader = pysam.VariantFile(vcf_file_path)
            for record in vcf_reader:
                if record.chrom != 'Y' and len(record.ref) == 1 and all(len(alt) == 1 for alt in record.alts):  # Exclude chromosome Y and select only SNVs
                    chrom = f'chr{record.chrom}' if not record.chrom.startswith('chr') else record.chrom
                    window_index = record.pos // window_size
                    patient_window_mutations[patient_id][chrom][window_index] += 1

# Normalize by the number of samples for each patient
for patient_id, chromosomes in patient_window_mutations.items():
    num_samples = len(patient_to_samples[patient_id])
    for chrom, windows in chromosomes.items():
        for window_index, count in windows.items():
            patient_window_mutations[patient_id][chrom][window_index] = count / num_samples

# Aggregate and normalize across all patients
aggregate_window_mutations = defaultdict(lambda: defaultdict(float))
for patient_id, chromosomes in patient_window_mutations.items():
    for chrom, windows in chromosomes.items():
        for window_index, normalized_count in windows.items():
            aggregate_window_mutations[chrom][window_index] += normalized_count

# Final normalization by total number of patients
for chrom, windows in aggregate_window_mutations.items():
    for window_index in windows:
        aggregate_window_mutations[chrom][window_index] /= total_patients

# Output or further processing of aggregate_window_mutations as needed
# Initialize the list to hold results
results_to_output = []

# Iterate over the aggregate_window_mutations structure
for chrom, windows in aggregate_window_mutations.items():
    for window_index, normalized_count in windows.items():
        # Construct the result dictionary for each chromosome and window
        result = {
            "chromosome": chrom,
            "window_index": window_index,
            "normalized_mutation_count": normalized_count
        }
        # Append the result dictionary to the list
        results_to_output.append(result)

# Define the output file path
output_file_path = "total_SNV_average_count.json"  # Adjust the path as necessary

# Write the results to a JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(results_to_output, json_file, indent=4)

print(f"Results have been outputted to {output_file_path}")
