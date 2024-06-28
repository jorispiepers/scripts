## PowershellFunctions.ps1

function ExtractTar {
	[CmdletBinding()]
	Param([Parameter(Mandatory=$true, Position=0)]
		[string]$newPath
	)
	
	# Test if tar files exist, in case so extract them
	$tarList = $(Get-ChildItem $newPath -Recurse -Include *.tar);
	
	if ($tarList.count -eq 0) {
		Write-Host "Error no .tar files found nothing to extract ..."
	} elseif (Test-Path 'C:\Program Files\7-Zip') {
		ForEach ($fileName in $tarList.FullName) {
			# Split filepath and tar archive so we can use it
			$filePath = $(Split-Path -Path $fileName -Parent -Resolve);
			$fileName = $(Split-Path -Path $fileName -Leaf -Resolve);
			
			# Create subfolder to store our Rice images
			$newFolder = $fileName.Split(".")[0];
			
			if (Test-Path -Path $filePath\DICOM) {
				Write-Host "Skipping folder creation ...";
			} else {
				New-Item -ItemType "directory" -Name $newFolder -Path $filePath;
			}
			
			$currentPath = $(Get-Location);
			cd $filePath\$newFolder;
			
			if (C:\Progra~1\7-Zip\7z.exe x $filePath\$fileName) {
				Write-Host "Decompression $filePath\$newFolder\$fileName okay ..."
				#Remove-Item $filePath\$newFolder\$fileName;
			} else {
				Write-Host "Decompression $filePath\$newFolder\$fileName failed!";
				return -2;
				exit;
			}
			
			cd $currentPath;
		}
	} else {
		Write-Host "Can't extract anything no 7zip .tar decompression tool available exiting script ...";
		return -1;
		exit;
	}
}

function ConvertDicom {
	[CmdletBinding()]
	Param([Parameter(Mandatory=$true, Position=0)]
		[string]$filePath
	)

	# DICOM extension
	$dcmExt = ".dcm";

	# Test if .img files exist, in case so convert them	
	$fileList = $(Get-ChildItem $filePath -Recurse -Include *.img);

	if ($fileList.count -ne 0) {
		ForEach ($fileName in $fileList.FullName) {
			# Split input paths and filenames
			$inputPath = $(Split-Path -Path $fileName -Parent -Resolve);
			$inputName = $(Split-Path -Path $fileName -Leaf -Resolve);

			# Create new DICOM folder to store all our DICOM images we converted
			if (Test-Path -Path $inputPath\DICOM) {
			} else {
				# Create a new DICOM folder under our input path
				Write-Host "Creating new folder $inputPath\DICOM";
				New-Item -ItemType "directory" -Name "DICOM" -Path $inputPath;
			}
			
			# Generate new dicom file name based on original name with .dcm extension
			$outputName = $inputPath + "\DICOM\" + $inputName.split(".")[0] + $dcmExt;
	
			# Convert our files
			if (C:\Progra~1\Carestream\system5\utils\tool_dcff.exe -i $inputPath\$inputName -E) {
				Write-Host "Extraction $inputPath\$inputName successful!";
			} elseif (C:\Progra~1\Carestream\system5\utils\tool_dicom.exe -i $inputPath\$inputName -o $outputName) {
				Write-Host "Decompressing $inputPath\$inputName successful!";
			} else {
				Write-Host "Decompression $inputPath\$inputName failed!";
			}
			
			# Move any leftover files into the DICOM folder
			Move-Item $inputPath\*.dcm $inputPath\DICOM;
		}
	}
}

function CompressArchive {
	[CmdletBinding()]
	Param([Parameter(Mandatory=$true, Position=0)]
		[string]$filePath
	)
	
	# Test if .dcm files exist, in case so compress them
	$fileList = $(Get-ChildItem $filePath -Recurse -Include DICOM);

	if ($fileList.count -ne 0) {
		ForEach ($folderPath in $fileList.FullName) {
			# Compression with 7zip
			if (Test-Path 'C:\Program Files\7-Zip')
			{
				$archiveFolder = $folderPath.Substring(0, $folderPath.Length - 6);
				$archiveName = $(Split-Path $archiveFolder -Leaf);
				
				$currentPath = $(Get-Location);
				cd $archiveFolder;
				
				C:\Progra~1\7-Zip\7z.exe a .\DICOM-$archiveName.7z -r .\DICOM -mx9 -v100m;
				Move-Item .\DICOM-$archiveName* $currentPath;
			} else {
				Write-Host "Zipping should be done manually, 7zip compression tools do not exist on this server ...";
				Write-Host "Folder $archiveFolder\DICOM could not be compressed ...";
			}
			cd $currentPath;
		}
	}
}

Clear-host;
$thisFolder = "C:\Temp\Joris";
$currentPath = $(Get-Location);
ExtractTar $currentPath;
ConvertDicom $currentPath;
CompressArchive $currentPath;

cd $currentPath;
Get-ChildItem;

# Get Service data
Get-Service | Where-Object Status -Match "Running"
Get-Service -DependentServices

# Get Drive information
Get-Disk

# Get memory information
Get-Counter '\Memory\Available Bytes'
Get-Counter '\Memory\Committed Bytes'
Get-Counter '\Processor(_Total)\% Processor Time'

# Return all counters related to memory
Get-Counter -ListSet *memory* | Select-Object -ExpandProperty  Counter

# Return all counters related to GPU
Get-Counter -ListSet *gpu* | Select-Object -ExpandProperty  Counter

# Return all counters related to PhysicalDisk/ physical network iface
Get-Counter -ListSet *phy* | Select-Object -ExpandProperty  Counter

# Return all counters related to Processor
Get-Counter -ListSet *processor* | Select-Object -ExpandProperty  Counter

# Get storage space
Get-PSDrive

$OS = Get-Ciminstance Win32_OperatingSystem
$cpuLoad = (Get-CimInstance win32_processor).LoadPercentage
$ramUsage = (100 - ($OS.FreePhysicalMemory / $OS.TotalVisibleMemorySize) * 100)

Write-Host $OS
Write-Host $cpuLoad
Write-Host $ramUsage

Get-EventLog -LogName Application
Get-EventLog -LogName Security
Get-EventLog -LogName System