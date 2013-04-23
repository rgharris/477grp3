%if errorType == "confirm":
<h2>Placement Confirmation</h2>
<p>Would you like to confirm the {{piece}} you just placed?</p>
<a href="javascript:runi2c('confirm');closeModal()" class="bottom half left">Yes</a>
<a href="javascript:closeModal()" class="bottom half right">No</a>

%elif errorType == "replace":
<h2>Piece Error</h2>
<p>Please replace the {{piece}} you removed.</p>

%elif errorType == "remove":
<h2>Piece Error</h2>
<p>Please remove the invalid {{piece}}.</p>

%end
