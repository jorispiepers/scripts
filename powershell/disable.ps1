foreach ($svc in Get-Service -Name Next*) {
	if ($svc.status -eq "Running") {
		Stop-Service -Name $svc.Name
	}
}

Get-PnpDevice | where {
	$_.friendlyname -like "Synaptics UWP WBDI"
} | Disable-PnPDevice

Get-PnPDevice | Where {
	$_.friendlyname -like "Intel® Smart Sound Technology for Digital Microphones"
} | Disable-PnPDevice