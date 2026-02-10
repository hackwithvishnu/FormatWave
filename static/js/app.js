/* ══════════════════════════════════════════════════════════════════════════════
   FormatWave — Frontend Application Logic
   Handles file upload, conversion, preview, and download
   ══════════════════════════════════════════════════════════════════════════════ */

(() => {
    'use strict';

    // ─── State ──────────────────────────────────────────────────────────────
    const state = {
        conversions: [],
        selectedConversion: null,
        selectedFiles: [],
        sessionId: null,
        results: [],
    };

    // ─── DOM Refs ───────────────────────────────────────────────────────────
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    const dom = {
        navbar: $('#navbar'),
        formatGrid: $('#formatGrid'),
        formatsGrid: $('#formatsGrid'),
        uploadZoneWrapper: $('#uploadZoneWrapper'),
        uploadZone: $('#uploadZone'),
        uploadAccepted: $('#uploadAccepted'),
        fileInput: $('#fileInput'),
        fileList: $('#fileList'),
        fileCount: $('#fileCount'),
        fileItems: $('#fileItems'),
        btnClear: $('#btnClear'),
        btnConvert: $('#btnConvert'),
        progressWrapper: $('#progressWrapper'),
        progressBar: $('#progressBar'),
        resultsWrapper: $('#resultsWrapper'),
        resultsTitle: $('#resultsTitle'),
        resultsSubtitle: $('#resultsSubtitle'),
        resultsErrors: $('#resultsErrors'),
        resultsGrid: $('#resultsGrid'),
        btnDownloadAll: $('#btnDownloadAll'),
        btnNewConversion: $('#btnNewConversion'),
        toastContainer: $('#toastContainer'),
    };

    // ─── Init ───────────────────────────────────────────────────────────────
    async function init() {
        await loadConversions();
        setupEventListeners();
        setupScrollEffects();
    }

    // ─── API: Load Conversions ──────────────────────────────────────────────
    async function loadConversions() {
        try {
            const res = await fetch('/api/conversions');
            const data = await res.json();
            state.conversions = data.conversions;
            renderFormatSelector();
            renderFormatsShowcase();
        } catch (err) {
            showToast('Failed to load conversion options', 'error');
            console.error(err);
        }
    }

    // ─── Render: Format Selector Cards ──────────────────────────────────────
    function renderFormatSelector() {
        dom.formatGrid.innerHTML = state.conversions.map((conv, i) => `
            <div class="format-card" data-id="${conv.id}" style="animation-delay: ${i * 0.05}s">
                <span class="format-card-icon">${conv.icon}</span>
                <div class="format-card-info">
                    <div class="format-card-name">
                        ${conv.from} <span class="format-arrow">→</span> ${conv.to}
                    </div>
                    <div class="format-card-desc">${conv.description}</div>
                </div>
                <div class="format-card-check">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                </div>
            </div>
        `).join('');
    }

    // ─── Render: Formats Showcase Section ───────────────────────────────────
    function renderFormatsShowcase() {
        dom.formatsGrid.innerHTML = state.conversions.map((conv, i) => `
            <div class="format-showcase-card" style="animation-delay: ${i * 0.08}s">
                <div class="format-showcase-icon">${conv.icon}</div>
                <div class="format-showcase-name">
                    ${conv.from} <span class="format-showcase-arrow">→</span> ${conv.to}
                </div>
                <div class="format-showcase-desc">${conv.description}</div>
            </div>
        `).join('');
    }

    // ─── Event Listeners ────────────────────────────────────────────────────
    function setupEventListeners() {
        // Format card selection
        dom.formatGrid.addEventListener('click', (e) => {
            const card = e.target.closest('.format-card');
            if (!card) return;

            const id = card.dataset.id;
            selectConversion(id);
        });

        // Upload zone click
        dom.uploadZone.addEventListener('click', () => {
            dom.fileInput.click();
        });

        // File input change
        dom.fileInput.addEventListener('change', (e) => {
            addFiles(Array.from(e.target.files));
            dom.fileInput.value = '';
        });

        // Drag & drop
        dom.uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dom.uploadZone.classList.add('drag-over');
        });

        dom.uploadZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dom.uploadZone.classList.remove('drag-over');
        });

        dom.uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dom.uploadZone.classList.remove('drag-over');
            addFiles(Array.from(e.dataTransfer.files));
        });

        // Clear files
        dom.btnClear.addEventListener('click', () => {
            clearFiles();
        });

        // Convert
        dom.btnConvert.addEventListener('click', () => {
            convertFiles();
        });

        // Download all
        dom.btnDownloadAll.addEventListener('click', () => {
            if (state.sessionId) {
                window.location.href = `/api/download-all/${state.sessionId}`;
            }
        });

        // New conversion
        dom.btnNewConversion.addEventListener('click', () => {
            resetToStart();
        });
    }

    // ─── Scroll Effects ─────────────────────────────────────────────────────
    function setupScrollEffects() {
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    dom.navbar.classList.toggle('scrolled', window.scrollY > 40);
                    ticking = false;
                });
                ticking = true;
            }
        });

        // Intersection observer for scroll animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, { threshold: 0.1 });

        $$('.format-showcase-card').forEach(card => {
            card.style.animationPlayState = 'paused';
            observer.observe(card);
        });
    }

    // ─── Select Conversion Type ─────────────────────────────────────────────
    function selectConversion(id) {
        const conv = state.conversions.find(c => c.id === id);
        if (!conv) return;

        state.selectedConversion = conv;
        state.selectedFiles = [];

        // Update UI
        $$('.format-card').forEach(card => {
            card.classList.toggle('active', card.dataset.id === id);
        });

        // Show upload zone
        dom.uploadZoneWrapper.style.display = 'block';
        dom.uploadZoneWrapper.style.animation = 'none';
        void dom.uploadZoneWrapper.offsetHeight; // Trigger reflow
        dom.uploadZoneWrapper.style.animation = 'fadeInUp 0.5s var(--ease-out) both';

        // Update accepted formats
        dom.uploadAccepted.innerHTML = conv.from_ext.map(ext =>
            `<span class="upload-accepted-badge">.${ext}</span>`
        ).join('');

        // Update file input accept attribute
        dom.fileInput.setAttribute('accept', conv.from_ext.map(e => `.${e}`).join(','));

        // Reset file list and results
        clearFiles();
        hideResults();
        hideProgress();

        // Scroll into view
        dom.uploadZoneWrapper.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // ─── File Management ────────────────────────────────────────────────────
    function addFiles(files) {
        if (!state.selectedConversion) {
            showToast('Please select a conversion type first', 'error');
            return;
        }

        const acceptedExts = state.selectedConversion.from_ext;

        files.forEach(file => {
            const ext = file.name.split('.').pop().toLowerCase();
            if (!acceptedExts.includes(ext)) {
                showToast(`${file.name}: Unsupported format (.${ext})`, 'error');
                return;
            }

            // Avoid duplicates
            if (state.selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                return;
            }

            state.selectedFiles.push(file);
        });

        renderFileList();
    }

    function removeFile(index) {
        state.selectedFiles.splice(index, 1);
        renderFileList();
    }

    function clearFiles() {
        state.selectedFiles = [];
        renderFileList();
    }

    function renderFileList() {
        const count = state.selectedFiles.length;

        if (count === 0) {
            dom.fileList.style.display = 'none';
            dom.btnConvert.style.display = 'none';
            return;
        }

        dom.fileList.style.display = 'block';
        dom.btnConvert.style.display = 'flex';
        dom.fileCount.textContent = count;

        dom.fileItems.innerHTML = state.selectedFiles.map((file, i) => `
            <div class="file-item" style="animation-delay: ${i * 0.05}s">
                <div class="file-item-icon">${getFileIcon(file.name)}</div>
                <div class="file-item-info">
                    <div class="file-item-name">${file.name}</div>
                    <div class="file-item-size">${humanSize(file.size)}</div>
                </div>
                <button class="file-item-remove" data-index="${i}" title="Remove file">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            </div>
        `).join('');

        // Add remove handlers
        dom.fileItems.querySelectorAll('.file-item-remove').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                removeFile(parseInt(btn.dataset.index));
            });
        });
    }

    // ─── Convert Files ──────────────────────────────────────────────────────
    async function convertFiles() {
        if (!state.selectedConversion || state.selectedFiles.length === 0) return;

        // Show progress
        showProgress();

        const formData = new FormData();
        formData.append('conversion_id', state.selectedConversion.id);
        state.selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        try {
            const res = await fetch('/api/convert', {
                method: 'POST',
                body: formData,
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || 'Conversion failed');
            }

            state.sessionId = data.session_id;
            state.results = data.results;

            // Small delay for visual smoothness
            await delay(800);

            hideProgress();
            showResults(data);

            if (data.total_converted > 0) {
                showToast(`Successfully converted ${data.total_converted} file(s)!`, 'success');
            }

        } catch (err) {
            hideProgress();
            showToast(err.message || 'Conversion failed', 'error');
            console.error(err);
        }
    }

    // ─── Show/Hide UI Sections ──────────────────────────────────────────────
    function showProgress() {
        dom.uploadZoneWrapper.style.display = 'none';
        dom.resultsWrapper.style.display = 'none';
        dom.progressWrapper.style.display = 'block';
    }

    function hideProgress() {
        dom.progressWrapper.style.display = 'none';
    }

    function showResults(data) {
        dom.resultsWrapper.style.display = 'block';
        dom.resultsWrapper.style.animation = 'none';
        void dom.resultsWrapper.offsetHeight;
        dom.resultsWrapper.style.animation = 'fadeInUp 0.5s var(--ease-out) both';

        dom.resultsSubtitle.textContent = `${data.total_converted} file(s) converted successfully`;

        // Download all button
        if (data.download_all_url) {
            dom.btnDownloadAll.style.display = 'inline-flex';
        } else {
            dom.btnDownloadAll.style.display = 'none';
        }

        // Errors
        if (data.errors && data.errors.length > 0) {
            dom.resultsErrors.style.display = 'block';
            dom.resultsErrors.innerHTML = data.errors.map(err =>
                `<div class="error-item"><strong>${err.filename}:</strong> ${err.error}</div>`
            ).join('');
        } else {
            dom.resultsErrors.style.display = 'none';
        }

        // Result cards
        dom.resultsGrid.innerHTML = data.results.map((result, i) => `
            <div class="result-card" style="animation-delay: ${i * 0.08}s">
                <div class="result-card-preview">
                    ${result.previewable
                ? `<img src="${result.preview_url}" alt="${result.converted_name}" loading="lazy">`
                : `<span class="no-preview">📄</span>`
            }
                </div>
                <div class="result-card-body">
                    <div class="result-card-name" title="${result.converted_name}">${result.converted_name}</div>
                    <div class="result-card-meta">
                        <span class="result-card-size">${result.size_human}</span>
                        <span class="result-card-from">from ${result.original_name}</span>
                    </div>
                    <button class="btn-download" onclick="window.location.href='${result.download_url}'">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                        Download
                    </button>
                </div>
            </div>
        `).join('');

        // Scroll to results
        dom.resultsWrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function hideResults() {
        dom.resultsWrapper.style.display = 'none';
    }

    function resetToStart() {
        state.selectedFiles = [];
        state.sessionId = null;
        state.results = [];

        hideResults();
        hideProgress();

        dom.uploadZoneWrapper.style.display = 'block';
        dom.uploadZoneWrapper.style.animation = 'none';
        void dom.uploadZoneWrapper.offsetHeight;
        dom.uploadZoneWrapper.style.animation = 'fadeInUp 0.5s var(--ease-out) both';

        clearFiles();

        dom.uploadZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // ─── Toast Notifications ────────────────────────────────────────────────
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span>${type === 'success' ? '✅' : '❌'}</span>
            <span>${message}</span>
        `;

        dom.toastContainer.appendChild(toast);

        // Auto dismiss
        setTimeout(() => {
            toast.classList.add('toast-out');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // ─── Helpers ────────────────────────────────────────────────────────────
    function humanSize(bytes) {
        const units = ['B', 'KB', 'MB', 'GB'];
        let i = 0;
        while (bytes >= 1024 && i < units.length - 1) {
            bytes /= 1024;
            i++;
        }
        return `${bytes.toFixed(1)} ${units[i]}`;
    }

    function getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const icons = {
            pdf: '📄', png: '🖼️', jpg: '🎨', jpeg: '🎨',
            webp: '🌐', bmp: '🗺️', tiff: '📷', tif: '📷',
            svg: '✏️',
        };
        return icons[ext] || '📁';
    }

    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // ─── Start ──────────────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', init);
})();
