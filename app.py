import io
import base64
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

# =============================================================================
# KONFIGURASI HALAMAN
# =============================================================================
st.set_page_config(
    page_title="Herbalife Customer Segmentation",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS - TAMPILAN MODERN
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main {
        background-color: #f6f8fb;
    }

    /* Metric card */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f4f7fb 100%);
        border-radius: 18px;
        padding: 22px 20px;
        box-shadow: 0 4px 18px rgba(31, 122, 90, 0.08);
        border: 1px solid rgba(31, 122, 90, 0.08);
        text-align: left;
        height: 100%;
        transition: transform .15s ease;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-icon { font-size: 28px; margin-bottom: 6px; }
    .metric-label {
        font-size: 13px; color: #6b7280; font-weight: 500;
        text-transform: uppercase; letter-spacing: .04em;
    }
    .metric-value {
        font-size: 26px; font-weight: 700; color: #14532d; margin-top: 2px;
    }
    .metric-sub { font-size: 12px; color: #9ca3af; margin-top: 4px; }

    /* Header banner */
    .header-banner {
        background: linear-gradient(120deg, #16a34a 0%, #15803d 45%, #166534 100%);
        padding: 28px 32px;
        border-radius: 20px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(21, 128, 61, 0.25);
    }
    .header-banner h1 { margin: 0; font-weight: 700; font-size: 28px; }
    .header-banner p { margin: 4px 0 0 0; opacity: .9; font-size: 14px; }

    /* Section title */
    .section-title {
        font-size: 19px; font-weight: 600; color: #14532d;
        margin: 6px 0 12px 0; border-left: 5px solid #16a34a; padding-left: 10px;
    }

    /* Cluster / strategy cards */
    .cluster-card {
        border-radius: 16px; padding: 20px; height: 100%;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-top: 5px solid var(--accent, #16a34a);
        background: white;
    }
    .cluster-card h4 { margin: 0 0 8px 0; color: #111827; }
    .cluster-card .badge {
        display:inline-block; padding: 3px 10px; border-radius: 999px;
        font-size: 11px; font-weight: 600; color: white;
        background: var(--accent, #16a34a); margin-bottom: 10px;
    }
    .cluster-card p { color: #4b5563; font-size: 13.5px; line-height: 1.5; }
    .cluster-card .stat-row { display:flex; justify-content: space-between; font-size:12.5px; color:#374151; margin-top:10px; border-top:1px dashed #e5e7eb; padding-top:8px;}

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3d24 0%, #14532d 100%);
    }
    div[data-testid="stSidebar"] * { color: #ecfdf5 !important; }
    div[data-testid="stSidebar"] .stRadio label { font-size: 14.5px; }

    .stButton>button, .stDownloadButton>button {
        border-radius: 10px; font-weight: 600; border: none;
        background: #16a34a; color: white; padding: 8px 18px;
    }
    .stButton>button:hover, .stDownloadButton>button:hover { background: #15803d; }
</style>
""", unsafe_allow_html=True)

CLUSTER_COLORS = {0: "#3b82f6", 1: "#f59e0b", 2: "#16a34a", 3: "#ef4444", 4: "#8b5cf6"}

STRATEGI = {
    0: {
        "Kategori": "Pelanggan Reguler",
        "Icon": "🙂",
        "Deskripsi": "Recency, Frequency, dan Monetary berada pada tingkat sedang. Pelanggan masih cukup aktif bertransaksi.",
        "Strategi": "Berikan promosi berkala, rekomendasi produk sesuai riwayat pembelian, dan program membership.",
    },
    1: {
        "Kategori": "Pelanggan Berisiko",
        "Icon": "⚠️",
        "Deskripsi": "Recency relatif tinggi, Frequency dan Monetary rendah. Sudah cukup lama tidak bertransaksi.",
        "Strategi": "Kirim voucher diskon, promo reaktivasi, serta pengingat untuk kembali melakukan pembelian.",
    },
    2: {
        "Kategori": "Pelanggan Loyal",
        "Icon": "⭐",
        "Deskripsi": "Recency paling rendah, Frequency & Monetary paling tinggi. Pelanggan terbaik dan paling aktif.",
        "Strategi": "Berikan reward, poin loyalitas, promo eksklusif, serta penawaran produk premium.",
    },
    3: {
        "Kategori": "Pelanggan Tidak Aktif",
        "Icon": "💤",
        "Deskripsi": "Recency paling tinggi, Frequency & Monetary paling rendah. Sudah lama tidak bertransaksi.",
        "Strategi": "Lakukan kampanye win-back, diskon besar, atau penawaran khusus untuk menarik pelanggan kembali.",
    },
    4: {
        "Kategori": "Pelanggan Potensial",
        "Icon": "🚀",
        "Deskripsi": "Frequency & Monetary cukup tinggi, Recency relatif rendah. Berpotensi menjadi pelanggan loyal.",
        "Strategi": "Tawarkan paket bundling, upselling, dan promosi produk baru agar nilai transaksi meningkat.",
    },
}

# =============================================================================
# LOAD & PROSES DATA (mengikuti alur notebook)
# =============================================================================
@st.cache_data(show_spinner=False)
def load_raw_data(file):
    df = pd.read_csv(file)
    df.drop_duplicates(inplace=True)
    df["Tanggal_Transaksi"] = pd.to_datetime(df["Tanggal_Transaksi"])
    return df


@st.cache_data(show_spinner=False)
def compute_rfm(df):
    snapshot_date = df["Tanggal_Transaksi"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("Customer_ID").agg(
        Recency=("Tanggal_Transaksi", lambda x: (snapshot_date - x.max()).days),
        Frequency=("Customer_ID", "size"),
        Monetary=("Total_Transaksi", "sum"),
    ).reset_index()
    return rfm, snapshot_date


@st.cache_data(show_spinner=False)
def run_elbow(X, k_range=range(2, 11)):
    wcss = []
    for i in k_range:
        km = KMeans(n_clusters=i, random_state=42, n_init=10)
        km.fit(X)
        wcss.append(km.inertia_)
    return list(k_range), wcss


@st.cache_data(show_spinner=False)
def run_kmeans(rfm, optimal_k=5):
    scaler = StandardScaler()
    X = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    rfm = rfm.copy()
    rfm["Cluster"] = labels
    return rfm, score, X


@st.cache_data(show_spinner=False)
def run_decision_tree(rfm):
    X_tree = rfm[["Recency", "Frequency", "Monetary"]]
    y_tree = rfm["Cluster"]
    X_train, X_test, y_train, y_test = train_test_split(
        X_tree, y_tree, test_size=0.3, random_state=42
    )
    tree_model = DecisionTreeClassifier(random_state=42, max_depth=4)
    tree_model.fit(X_train, y_train)
    y_pred = tree_model.predict(X_test)
    akurasi = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred, labels=sorted(y_tree.unique()))
    return tree_model, akurasi, cm, X_train, X_test, y_train, y_test, y_pred


@st.cache_data(show_spinner=False)
def render_tree_image(_tree_model, class_labels):
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(
        _tree_model,
        feature_names=["Recency", "Frequency", "Monetary"],
        class_names=class_labels,
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax,
    )
    ax.set_title("Visualisasi Decision Tree untuk Prediksi Cluster Pelanggan", fontsize=14)
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def metric_card(icon, label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## 🌿 Herbalife Analytics")
    st.caption("Segmentasi Pelanggan berbasis RFM & K-Means")
    st.markdown("---")

    uploaded = st.file_uploader("📁 Ganti dataset (opsional)", type=["csv"])
    data_source = uploaded if uploaded is not None else "dataset_herbalife2425_koreksi.csv"

    page = st.radio(
        "Navigasi",
        [
            "🏠 Dashboard Utama",
            "🌳 Decision Tree",
            "🎯 Strategi Pemasaran",
            "📄 Data Mentah",
        ],
    )
    st.markdown("---")
    st.caption("Dibuat dari notebook analisis RFM + K-Means + Decision Tree")

# =============================================================================
# PIPELINE DATA
# =============================================================================
try:
    herbal = load_raw_data(data_source)
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

rfm_raw, snapshot_date = compute_rfm(herbal)
rfm, sil_score, X_scaled = run_kmeans(rfm_raw, optimal_k=5)
rfm["Kategori"] = rfm["Cluster"].map(lambda c: STRATEGI[c]["Kategori"])

tree_model, akurasi, cm, X_train, X_test, y_train, y_test, y_pred = run_decision_tree(rfm)

cluster_summary = rfm.groupby("Cluster").agg(
    Recency=("Recency", "mean"),
    Frequency=("Frequency", "mean"),
    Monetary=("Monetary", "mean"),
    Jumlah_Pelanggan=("Customer_ID", "count"),
).reset_index()

# =============================================================================
# HEADER
# =============================================================================
st.markdown("""
<div class="header-banner">
    <h1>🌿 Herbalife Customer Segmentation Dashboard</h1>
    <p>Analisis RFM (Recency, Frequency, Monetary) · Segmentasi K-Means · Prediksi Decision Tree</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# HALAMAN 1: DASHBOARD UTAMA
# =============================================================================
if page == "🏠 Dashboard Utama":

    # ---- Metric cards ----
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("👥", "Total Pelanggan", f"{rfm.shape[0]:,}".replace(",", "."))
    with c2:
        metric_card("🧾", "Total Transaksi", f"{herbal.shape[0]:,}".replace(",", "."))
    with c3:
        metric_card("💰", "Total Revenue", rupiah(herbal["Total_Transaksi"].sum()))
    with c4:
        metric_card("📊", "Rata-rata Nilai Transaksi", rupiah(herbal["Total_Transaksi"].mean()))
    with c5:
        metric_card("🧩", "Jumlah Cluster", "5", sub=f"Silhouette: {sil_score:.3f}")

    st.write("")

    # ---- Filter & Search ----
    st.markdown('<div class="section-title">🔍 Pencarian & Filter</div>', unsafe_allow_html=True)
    fcol1, fcol2 = st.columns([2, 3])
    with fcol1:
        search_id = st.text_input("Cari Customer ID", placeholder="Contoh: C0101")
    with fcol2:
        cluster_options = sorted(rfm["Cluster"].unique())
        chosen_clusters = st.multiselect(
            "Filter berdasarkan Cluster",
            options=cluster_options,
            default=cluster_options,
            format_func=lambda c: f"Cluster {c} - {STRATEGI[c]['Kategori']}",
        )

    filtered = rfm[rfm["Cluster"].isin(chosen_clusters)]
    if search_id:
        filtered = filtered[filtered["Customer_ID"].str.contains(search_id.strip(), case=False, na=False)]

    st.caption(f"Menampilkan **{filtered.shape[0]}** dari {rfm.shape[0]} pelanggan")

    # ---- Tabel ----
    st.dataframe(
        filtered.sort_values("Monetary", ascending=False).style.format({
            "Monetary": "Rp {:,.0f}",
            "Recency": "{:.0f}",
            "Frequency": "{:.0f}",
        }),
        width='stretch',
        height=320,
    )

    # ---- Download ----
    csv_buffer = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Hasil Clustering (CSV)",
        data=csv_buffer,
        file_name="hasil_clustering_herbalife.csv",
        mime="text/csv",
    )

    st.write("")
    st.markdown('<div class="section-title">📊 Visualisasi Segmentasi</div>', unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        fig_scatter = px.scatter(
            filtered,
            x="Frequency", y="Monetary",
            color=filtered["Cluster"].astype(str),
            color_discrete_map={str(k): v for k, v in CLUSTER_COLORS.items()},
            hover_data=["Customer_ID", "Recency", "Kategori"],
            title="Frequency vs Monetary per Cluster",
            labels={"color": "Cluster"},
        )
        fig_scatter.update_traces(marker=dict(size=9, opacity=0.8, line=dict(width=0.5, color="white")))
        fig_scatter.update_layout(template="plotly_white", height=420, legend_title_text="Cluster")
        st.plotly_chart(fig_scatter, width='stretch')

    with g2:
        count_df = rfm["Cluster"].value_counts().sort_index().reset_index()
        count_df.columns = ["Cluster", "Jumlah"]
        count_df["Kategori"] = count_df["Cluster"].map(lambda c: STRATEGI[c]["Kategori"])
        fig_pie = px.pie(
            count_df, names="Kategori", values="Jumlah",
            color="Cluster", color_discrete_map=CLUSTER_COLORS,
            title="Proporsi Pelanggan per Segmen", hole=0.45,
        )
        fig_pie.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig_pie, width='stretch')

    g3, g4 = st.columns(2)
    with g3:
        fig_bar = px.bar(
            cluster_summary, x="Cluster", y="Jumlah_Pelanggan",
            color=cluster_summary["Cluster"].astype(str),
            color_discrete_map={str(k): v for k, v in CLUSTER_COLORS.items()},
            text="Jumlah_Pelanggan",
            title="Jumlah Pelanggan per Cluster",
        )
        fig_bar.update_layout(template="plotly_white", height=400, showlegend=False)
        st.plotly_chart(fig_bar, width='stretch')

    with g4:
        fig_rfm = go.Figure()
        for _, row in cluster_summary.iterrows():
            fig_rfm.add_trace(go.Scatterpolar(
                r=[row["Recency"], row["Frequency"], row["Monetary"] / max(cluster_summary["Monetary"].max(), 1) * 100],
                theta=["Recency", "Frequency", "Monetary (scaled)"],
                fill="toself",
                name=f"Cluster {int(row['Cluster'])}",
                line_color=CLUSTER_COLORS[int(row["Cluster"])],
            ))
        fig_rfm.update_layout(
            template="plotly_white", height=400,
            title="Profil RFM Rata-rata per Cluster (radar)",
            polar=dict(radialaxis=dict(visible=True)),
        )
        st.plotly_chart(fig_rfm, width='stretch')

    st.markdown('<div class="section-title">📋 Ringkasan Karakteristik Cluster</div>', unsafe_allow_html=True)
    summary_display = cluster_summary.copy()
    summary_display["Kategori"] = summary_display["Cluster"].map(lambda c: STRATEGI[c]["Kategori"])
    summary_display = summary_display[["Cluster", "Kategori", "Recency", "Frequency", "Monetary", "Jumlah_Pelanggan"]]
    st.dataframe(
        summary_display.style.format({"Recency": "{:.1f} hari", "Frequency": "{:.1f}x", "Monetary": "Rp {:,.0f}"}),
        width='stretch',
    )

# =============================================================================
# HALAMAN 2: DECISION TREE
# =============================================================================
elif page == "🌳 Decision Tree":
    st.markdown('<div class="section-title">🌳 Model Decision Tree - Klasifikasi Cluster</div>', unsafe_allow_html=True)
    st.write(
        "Decision Tree dilatih untuk mempelajari aturan klasifikasi cluster pelanggan "
        "berdasarkan nilai **Recency, Frequency, dan Monetary** hasil segmentasi K-Means."
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("🎯", "Akurasi Model", f"{akurasi*100:.2f}%")
    with m2:
        metric_card("🌱", "Kedalaman Maksimum", "4")
    with m3:
        metric_card("🧪", "Data Training", f"{X_train.shape[0]}")
    with m4:
        metric_card("🧫", "Data Testing", f"{X_test.shape[0]}")

    st.write("")
    col_tree, col_side = st.columns([2.3, 1])

    with col_tree:
        st.markdown("#### 🖼️ Visualisasi Pohon Keputusan")
        class_labels = [str(c) for c in sorted(rfm["Cluster"].unique())]
        img_buf = render_tree_image(tree_model, class_labels)
        st.image(img_buf, width='stretch')
        st.download_button(
            "📥 Download Gambar Decision Tree",
            data=img_buf.getvalue(),
            file_name="decision_tree_herbalife.png",
            mime="image/png",
        )

    with col_side:
        st.markdown("#### 📌 Feature Importance")
        fi = pd.DataFrame({
            "Fitur": ["Recency", "Frequency", "Monetary"],
            "Importance": tree_model.feature_importances_,
        }).sort_values("Importance", ascending=True)
        fig_fi = px.bar(
            fi, x="Importance", y="Fitur", orientation="h",
            color="Importance", color_continuous_scale="Greens",
            text=fi["Importance"].round(3),
        )
        fig_fi.update_layout(template="plotly_white", height=260, showlegend=False, coloraxis_showscale=False,
                              margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_fi, width='stretch')

        st.markdown("#### 🔎 Confusion Matrix")
        labels_sorted = sorted(rfm["Cluster"].unique())
        fig_cm = px.imshow(
            cm, text_auto=True, color_continuous_scale="Greens",
            x=[f"Pred {c}" for c in labels_sorted], y=[f"Aktual {c}" for c in labels_sorted],
        )
        fig_cm.update_layout(template="plotly_white", height=280, margin=dict(l=10, r=10, t=10, b=10),
                              coloraxis_showscale=False)
        st.plotly_chart(fig_cm, width='stretch')

    st.markdown('<div class="section-title">📈 Perbandingan Jumlah Cluster (Elbow Method)</div>', unsafe_allow_html=True)
    scaler_tmp = StandardScaler()
    X_elbow = scaler_tmp.fit_transform(rfm_raw[["Recency", "Frequency", "Monetary"]])
    k_range, wcss = run_elbow(X_elbow)
    fig_elbow = px.line(x=list(k_range), y=wcss, markers=True,
                         labels={"x": "Jumlah Cluster (K)", "y": "WCSS"},
                         title="Elbow Method untuk Menentukan Jumlah Cluster Optimal")
    fig_elbow.add_vline(x=5, line_dash="dash", line_color="#16a34a", annotation_text="K optimal = 5")
    fig_elbow.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_elbow, width='stretch')
    st.caption(f"Silhouette Score untuk K=5: **{sil_score:.4f}**")

# =============================================================================
# HALAMAN 3: STRATEGI PEMASARAN
# =============================================================================
elif page == "🎯 Strategi Pemasaran":
    st.markdown('<div class="section-title">🎯 Strategi Pemasaran per Segmen Pelanggan</div>', unsafe_allow_html=True)
    st.write("Rekomendasi strategi pemasaran disusun berdasarkan karakteristik RFM tiap cluster hasil segmentasi.")

    cols = st.columns(3)
    for i, c in enumerate(sorted(STRATEGI.keys())):
        info = STRATEGI[c]
        row = cluster_summary[cluster_summary["Cluster"] == c].iloc[0]
        with cols[i % 3]:
            st.markdown(f"""
            <div class="cluster-card" style="--accent:{CLUSTER_COLORS[c]}">
                <span class="badge">Cluster {c}</span>
                <h4>{info['Icon']} {info['Kategori']}</h4>
                <p><b>Karakteristik:</b> {info['Deskripsi']}</p>
                <p><b>Strategi:</b> {info['Strategi']}</p>
                <div class="stat-row"><span>👥 {int(row['Jumlah_Pelanggan'])} pelanggan</span><span>⏱ {row['Recency']:.0f} hari</span></div>
                <div class="stat-row"><span>🔁 {row['Frequency']:.1f}x beli</span><span>💰 {rupiah(row['Monetary'])}</span></div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

    st.write("")
    st.markdown('<div class="section-title">📊 Perbandingan Nilai RFM Antar Segmen</div>', unsafe_allow_html=True)
    comp = cluster_summary.copy()
    comp["Kategori"] = comp["Cluster"].map(lambda c: STRATEGI[c]["Kategori"])
    t1, t2, t3 = st.columns(3)
    with t1:
        fig_r = px.bar(comp, x="Kategori", y="Recency", color="Kategori",
                        color_discrete_map={STRATEGI[c]["Kategori"]: CLUSTER_COLORS[c] for c in STRATEGI},
                        title="Rata-rata Recency (hari)")
        fig_r.update_layout(template="plotly_white", height=340, showlegend=False, xaxis_tickangle=-25)
        st.plotly_chart(fig_r, width='stretch')
    with t2:
        fig_f = px.bar(comp, x="Kategori", y="Frequency", color="Kategori",
                        color_discrete_map={STRATEGI[c]["Kategori"]: CLUSTER_COLORS[c] for c in STRATEGI},
                        title="Rata-rata Frequency (kali beli)")
        fig_f.update_layout(template="plotly_white", height=340, showlegend=False, xaxis_tickangle=-25)
        st.plotly_chart(fig_f, width='stretch')
    with t3:
        fig_m = px.bar(comp, x="Kategori", y="Monetary", color="Kategori",
                        color_discrete_map={STRATEGI[c]["Kategori"]: CLUSTER_COLORS[c] for c in STRATEGI},
                        title="Rata-rata Monetary (Rp)")
        fig_m.update_layout(template="plotly_white", height=340, showlegend=False, xaxis_tickangle=-25)
        st.plotly_chart(fig_m, width='stretch')

    st.write("")
    strategi_table = pd.DataFrame(STRATEGI).T[["Kategori", "Strategi"]]
    strategi_table.index.name = "Cluster"
    st.dataframe(strategi_table, width='stretch')

    csv_strategi = rfm.merge(
        pd.DataFrame(STRATEGI).T[["Kategori", "Strategi"]].reset_index().rename(columns={"index": "Cluster"}),
        on="Kategori", how="left", suffixes=("", "_ref")
    ) if False else rfm.copy()
    csv_strategi["Strategi_Pemasaran"] = csv_strategi["Cluster"].map(lambda c: STRATEGI[c]["Strategi"])
    st.download_button(
        "📥 Download Data Pelanggan + Strategi (CSV)",
        data=csv_strategi.to_csv(index=False).encode("utf-8"),
        file_name="pelanggan_strategi_pemasaran.csv",
        mime="text/csv",
    )

# =============================================================================
# HALAMAN 4: DATA MENTAH
# =============================================================================
elif page == "📄 Data Mentah":
    st.markdown('<div class="section-title">📄 Data Transaksi Mentah</div>', unsafe_allow_html=True)
    st.dataframe(herbal, width='stretch', height=420)
    st.caption(f"Total {herbal.shape[0]} baris transaksi setelah pembersihan duplikat.")

    st.markdown('<div class="section-title">📄 Data RFM per Pelanggan</div>', unsafe_allow_html=True)
    st.dataframe(rfm, width='stretch', height=420)

    st.download_button(
        "📥 Download Data RFM Lengkap (CSV)",
        data=rfm.to_csv(index=False).encode("utf-8"),
        file_name="rfm_herbalife.csv",
        mime="text/csv",
    )
