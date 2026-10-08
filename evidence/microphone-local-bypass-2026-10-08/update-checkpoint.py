"""Preserve every parent binding and bind this actual WIP continuation."""
import hashlib
import json
import subprocess
from pathlib import Path

folder = Path(__file__).resolve().parent
root = folder.parents[1]
read = lambda name: json.loads((folder / name).read_text())
summary = read('final-qualification-summary.json')
checkpoint_path = root / 'context/build-checkpoint.json'
checkpoint = json.loads(checkpoint_path.read_text())
relative = folder.relative_to(root).as_posix()
checkpoint.update({
    'native_build': relative + '/native-circuit.json.gz',
    'sha256': summary['native_sha256'], 'size_bytes': summary['native_bytes'],
    'traces': summary['native_traces'], 'vias': summary['native_vias'],
    'native_pours': summary['native_pours'], 'native_open_port_errors': summary['native_errors'],
    'physically_open_nets': summary['physically_open_nets'],
    'measured_geometry_violations': 0, 'measured_shorts': 0,
    'authored_region_widths_checked': 250, 'authored_region_width_failures': 0,
    'current_local_version': summary['version'], 'fabrication_ready': False,
    'native_wire_segments_width_checked': summary['native_wire_segments_checked'],
    'stationary_purchased_world_geometry_unchanged': 123, 'authorized_purchased_pose_moves': 2,
    'local_microphone_bypass': {k: v for k, v in summary.items() if k.startswith('local_bypass_')},
    'electrical_decoupling_placement_qualified': False,
    'latest_order_readiness_review': relative + '/review.md',
    'latest_accepted_correction': relative + '/review.md',
    'accepted_source_snapshot': relative + '/completed-source-and-events.tar.gz',
    'accepted_source_manifest': relative + '/generation-source-manifest.json',
    'source_snapshot_byte_verified': True,
    'publication_runtime_cli_build_seconds': 266.04,
    'publication_runtime_cli_build_passed': False,
    'publication_runtime_cli_build_error_count': 50,
    'publication_runtime_physical_records_identical': False,
    'current_publication_source_matches_checked_runtime': True,
    'publication_runtime_snapshot_seconds': 58.76,
    'publication_runtime_snapshot_receipt': relative + '/source-snapshot.log.outcome.json',
    'source_entry_snapshot_seconds': 58.76,
    'source_entry_snapshot_receipt': relative + '/source-snapshot.log.outcome.json',
    'publication_runtime_snapshot_passed': False, 'source_entry_snapshot_passed': False,
    'source_checks_receipt': relative + '/final-source-checks/source-checks.json',
    'code_checks_receipt': relative + '/artifact-checks.json',
    'native_qualification_receipt': relative + '/final-qualification-summary.json',
    'remaining_native_error_receipt': relative + '/remaining-native-errors.json',
    'latest_actual_srj': relative + '/final-native.srj.json',
    'current_native_component_inventory': relative + '/component-summary.json',
    'resolved_bom_receipt': relative + '/resolved-bom-receipt.json',
    'schematic_component_coverage_receipt': relative + '/guide-coverage.json',
    'latest_schematic_annotation_review': relative + '/guide-coverage.json',
    'final_visual_review': relative + '/visual-review.json',
    'ui_schematic_style_receipt': relative + '/ui-analysis/ui-style-analysis-receipt.json',
    'current_supplier_stock_verified': False,
    'supplier_stock_receipt': relative + '/official-stock/receipt.json',
    'supplier_stock_interpretation': relative + '/dated-stock-application.json',
    'supplier_current_identity_binding_receipt': relative + '/dated-stock-application.json',
    'dated_stock_identity_binding': relative + '/dated-stock-application.json',
    'supplier_confirmed_stock_covers_identities': 12,
    'supplier_inventory_unknown_identities': 29,
    'supplier_out_of_stock': ['C94934'],
    'supplier_zero_public_buyability': ['C2913201', 'C94934'],
    'genuine_supplier_orientation_cache_inputs': 43,
    'supplier_orientation_cache_receipt': relative + '/restored-supplier-cache.json',
    'previous_publication_cloud_CI_status': 'completed with null user_code_job_error; source script exit 0; does not qualify board DRC/fabrication',
    'previous_publication_cloud_CI_observation_receipt': relative + '/previous-cloud-completed-build.json',
    'public_fields_describe_parent_until_new_publication_verified': True,
    'cloud_setup_receipt': relative + '/cloud-setup-smoke/receipt.json',
    'supervisor_smoke_receipt': relative + '/cloud-setup-smoke/receipt.json',
    'limitations': [
        '50 native J7/U27 errors / 12 assigned physical open nets; J3 two unassigned outer contacts are additional unresolved connections.',
        'Requested centered approximately 2.8-inch landscape LCD unimplemented; exact mating/fold/bend/RF/common-cathode backlight remains unqualified.',
        '169 schema failures, 32 missing native paste records, polygon Gerber/official-short-check failures, U14 supplier rotation; latest core .2110 lacks tested paste fix.',
        'Two regulator routes below explicit width minima; 65 nominal-width discrepancies need current/thermal and signal-integrity qualification.',
        'Current official stock: only 12/43 covering identities confirmed; U1/D2 zero public buyability, 29 inventory results unknown HTTP503; no assembler allocation.',
        'Actual UI style 15 issues; source snapshots fail against unchanged references; no full zero-DRC/connectivity, fabrication, order or hardware-test approval.',
    ],
})
registry_file = folder / 'final-registry-receipt.json'
preview_file = folder / 'final-public-preview-receipt.json'
github_file = folder / 'github-publication-receipt.json'
if registry_file.exists() and preview_file.exists() and github_file.exists():
    registry = read('final-registry-receipt.json')
    preview = read('final-public-preview-receipt.json')
    github = read('github-publication-receipt.json')
    assert registry['complete_public_upload'] and preview['exact_native_object_equality']
    assert preview['local_native_json_sha256'] == summary['native_sha256']
    assert github['matching_files'] == github['checked_files'] == 128
    assert github['main_matches'] and not github['repository_is_private']
    checkpoint.update({
        'public_source_commit': github['commit'],
        'public_package_version': summary['version'],
        'public_package_release_id': preview['release_id'],
        'public_package_files_verified': 128,
        'public_package_all_bytes_match': True,
        'public_native_preview_exact_object_match': True,
        'public_preview_url': preview['preview_page_url'],
        'public_package_publication_receipt': relative + '/final-registry-receipt.json',
        'public_package_preview_receipt': relative + '/final-public-preview-receipt.json',
        'public_github_publication_receipt': relative + '/github-publication-receipt.json',
        'public_package_ready_to_build': registry['ready_to_build'],
        'public_package_is_private': registry['is_private'],
        'public_package_is_unlisted': registry['is_unlisted'],
        'public_package_cloud_build_id': None,
        'public_package_cloud_CI_passed': False,
        'public_package_cloud_CI_status': 'New .10 cloud job is a separate unverified source build until actual completed logs are read; exact public uploaded source/native/preview verification does not imply CI or fabrication approval.',
        'public_package_cloud_CI_observation_receipt': None,
        'public_package_cloud_CI_started_at': None,
        'public_fields_describe_parent_until_new_publication_verified': False,
    })
    if (folder / 'cloud-source-build-observation.json').exists():
        observed = read('cloud-source-build-observation.json')['response']['package_build']
        checkpoint.update({
            'public_package_cloud_build_id': observed['package_build_id'],
            'public_package_cloud_CI_status': 'Actual .10 automatic cloud job failed user_code_job_infrastructure_error before source execution; exact uploaded preview verified independently. One supported owned-release rebuild may be recorded separately.',
            'public_package_cloud_CI_observation_receipt': relative + '/cloud-source-build-observation.json',
            'public_package_cloud_CI_started_at': observed['user_code_job_started_at'],
        })
    if (folder / 'cloud-rebuild-request.json').exists():
        retry = read('cloud-rebuild-request.json')
        checkpoint['public_package_cloud_build_id'] = retry['package_build_id']
        checkpoint['public_package_cloud_CI_status'] = 'Both automatic .10 jobs failed platform sandbox initialization before source execution. One supported owned-release rebuild requested after exact public file verification; result unverified until actual completed logs are read.'
        checkpoint['public_package_cloud_rebuild_receipt'] = relative + '/cloud-rebuild-request.json'
    if (folder / 'cloud-rebuild-observation.json').exists():
        retry = read('cloud-rebuild-observation.json')['response']['package_build']
        checkpoint['public_package_cloud_CI_observation_receipt'] = relative + '/cloud-rebuild-observation.json'
        checkpoint['public_package_cloud_CI_started_at'] = retry['user_code_job_started_at']
        if retry['user_code_job_completed_at']:
            checkpoint['public_package_cloud_CI_passed'] = retry['user_code_job_error'] is None
            checkpoint['public_package_cloud_CI_status'] = 'Supported .10 rebuild completed; actual user-code job error: ' + json.dumps(retry['user_code_job_error']) + '; does not qualify board DRC/fabrication.'
        else:
            checkpoint['public_package_cloud_CI_status'] = 'Supported .10 rebuild genuinely started after two infrastructure failures; completion not observed, no CI/fabrication approval inferred.'
if (folder / 'cloud-configuration-save-receipt.json').exists():
    saved = read('cloud-configuration-save-receipt.json')
    checkpoint['cloud_configuration_saved_revision'] = saved['confirmed_revision']
    checkpoint['cloud_configuration_save_receipt'] = relative + '/cloud-configuration-save-receipt.json'
    checkpoint['cloud_configuration_applied'] = False
    checkpoint['cloud_environment_published'] = False
checkpoint_path.write_text(json.dumps(checkpoint, indent=2) + '\n')

parent = read('parent-checkpoint-sha256.json')
bindings = dict(parent['files'])
changed = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=root, text=True).splitlines()
paths = set(changed) | {p.relative_to(root).as_posix() for p in folder.rglob('*') if p.is_file()}
paths |= {'CLOUD_HANDOFF.md', 'context/build-checkpoint.json',
          'context/user-decisions.md', 'dist/placement/circuit.json'}
paths |= {p.relative_to(root / '.publish/board').as_posix()
          for p in (root / '.publish/board').rglob('*') if p.is_file()}
paths.discard('context/checkpoint-sha256.json')
for name in paths:
    path = root / name
    if path.is_file(): bindings[name] = hashlib.sha256(path.read_bytes()).hexdigest()
manifest = {
    'algorithm': 'sha256', 'accepted_version': summary['version'],
    'native_sha256': summary['native_sha256'],
    'classification': 'Actual qualified local microphone WIP .10. Full-board connection/DRC/fabrication gates remain failed. Publication verified independently.',
    'parent_manifest_archive': relative + '/parent-checkpoint-sha256.json',
    'parent_bound_file_count': len(parent['files']),
    'scope': 'Preserve every parent binding; add actual task changes, new evidence and all regular publication runtime paths; manifest excludes itself.',
    'files': dict(sorted(bindings.items())),
}
(root / 'context/checkpoint-sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'bound_files': len(bindings), 'parent_bound_files': len(parent['files']), 'native_sha256': summary['native_sha256']}))
