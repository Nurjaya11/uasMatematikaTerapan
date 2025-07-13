import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="Matematika Terapan untuk Perusahaan",
    page_icon="📊",
    layout="wide"
)

# Judul aplikasi
st.title("📊 Aplikasi Matematika Terapan untuk Perusahaan")
st.markdown("---")

# Sidebar untuk navigasi
st.sidebar.title("Menu Metode")
metode = st.sidebar.selectbox(
    "Pilih Metode Matematika:",
    ["EOQ (Economic Order Quantity)", "Break Even Point", "NPV & IRR", "Regresi Linear", "Optimasi Linear"]
)

# Fungsi untuk EOQ
def hitung_eoq():
    st.header("🔢 Economic Order Quantity (EOQ)")
    st.markdown("EOQ adalah metode untuk menentukan jumlah pesanan optimal yang meminimalkan total biaya persediaan.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameter")
        D = st.number_input("Permintaan Tahunan (D)", value=1000, min_value=1)
        K = st.number_input("Biaya Pesan per Order (K)", value=50, min_value=0.01)
        h = st.number_input("Biaya Penyimpanan per Unit per Tahun (h)", value=2, min_value=0.01)
        
        # Hitung EOQ
        if st.button("Hitung EOQ"):
            eoq = math.sqrt((2 * D * K) / h)
            total_cost = (D * K / eoq) + (eoq * h / 2)
            freq = D / eoq
            
            st.success(f"EOQ = {eoq:.2f} unit")
            st.success(f"Total Biaya = Rp {total_cost:,.2f}")
            st.success(f"Frekuensi Pesan = {freq:.2f} kali/tahun")
    
    with col2:
        st.subheader("Rumus EOQ")
        st.latex(r"EOQ = \sqrt{\frac{2DK}{h}}")
        st.markdown("""
        **Keterangan:**
        - D = Permintaan tahunan
        - K = Biaya pesan per order
        - h = Biaya penyimpanan per unit per tahun
        """)
        
        # Grafik EOQ
        if st.button("Tampilkan Grafik"):
            q_range = np.linspace(50, 500, 100)
            ordering_cost = (D * K) / q_range
            holding_cost = (q_range * h) / 2
            total_cost_range = ordering_cost + holding_cost
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(q_range, ordering_cost, label='Biaya Pesan', color='blue')
            ax.plot(q_range, holding_cost, label='Biaya Penyimpanan', color='green')
            ax.plot(q_range, total_cost_range, label='Total Biaya', color='red', linewidth=2)
            
            eoq_val = math.sqrt((2 * D * K) / h)
            ax.axvline(x=eoq_val, color='orange', linestyle='--', label=f'EOQ = {eoq_val:.2f}')
            
            ax.set_xlabel('Jumlah Pesanan (Q)')
            ax.set_ylabel('Biaya')
            ax.set_title('Grafik EOQ')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)

# Fungsi untuk Break Even Point
def hitung_bep():
    st.header("⚖️ Break Even Point (BEP)")
    st.markdown("BEP adalah titik dimana total pendapatan sama dengan total biaya.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameter")
        fixed_cost = st.number_input("Biaya Tetap (Fixed Cost)", value=100000, min_value=0)
        variable_cost = st.number_input("Biaya Variabel per Unit", value=5000, min_value=0)
        selling_price = st.number_input("Harga Jual per Unit", value=10000, min_value=0.01)
        
        if st.button("Hitung BEP"):
            if selling_price > variable_cost:
                bep_unit = fixed_cost / (selling_price - variable_cost)
                bep_rupiah = bep_unit * selling_price
                
                st.success(f"BEP (Unit) = {bep_unit:.2f} unit")
                st.success(f"BEP (Rupiah) = Rp {bep_rupiah:,.2f}")
                
                # Margin of Safety
                target_sales = st.number_input("Target Penjualan (unit)", value=100, min_value=0)
                if target_sales > bep_unit:
                    margin_safety = ((target_sales - bep_unit) / target_sales) * 100
                    st.info(f"Margin of Safety = {margin_safety:.2f}%")
            else:
                st.error("Harga jual harus lebih besar dari biaya variabel!")
    
    with col2:
        st.subheader("Rumus BEP")
        st.latex(r"BEP_{unit} = \frac{FC}{P - VC}")
        st.latex(r"BEP_{rupiah} = BEP_{unit} \times P")
        st.markdown("""
        **Keterangan:**
        - FC = Fixed Cost (Biaya Tetap)
        - P = Price (Harga Jual)
        - VC = Variable Cost (Biaya Variabel)
        """)
        
        # Grafik BEP
        if st.button("Tampilkan Grafik BEP"):
            units = np.linspace(0, 200, 100)
            total_cost = fixed_cost + (variable_cost * units)
            total_revenue = selling_price * units
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(units, total_cost, label='Total Biaya', color='red')
            ax.plot(units, total_revenue, label='Total Pendapatan', color='blue')
            
            bep_unit = fixed_cost / (selling_price - variable_cost)
            ax.axvline(x=bep_unit, color='green', linestyle='--', label=f'BEP = {bep_unit:.2f} unit')
            ax.axhline(y=fixed_cost, color='orange', linestyle=':', label='Fixed Cost')
            
            ax.set_xlabel('Unit Terjual')
            ax.set_ylabel('Rupiah')
            ax.set_title('Grafik Break Even Point')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)

# Fungsi untuk NPV & IRR
def hitung_npv_irr():
    st.header("💰 Net Present Value (NPV) & Internal Rate of Return (IRR)")
    st.markdown("NPV dan IRR adalah metode evaluasi investasi.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Parameter")
        initial_investment = st.number_input("Investasi Awal", value=1000000, min_value=0)
        discount_rate = st.number_input("Tingkat Diskonto (%)", value=10, min_value=0.01, max_value=100) / 100
        years = st.number_input("Jumlah Tahun", value=5, min_value=1, max_value=20)
        
        cash_flows = []
        st.subheader("Arus Kas Tahunan")
        for i in range(int(years)):
            cf = st.number_input(f"Tahun {i+1}", value=300000, key=f"cf_{i}")
            cash_flows.append(cf)
        
        if st.button("Hitung NPV & IRR"):
            # Hitung NPV
            npv = -initial_investment
            for i, cf in enumerate(cash_flows):
                npv += cf / ((1 + discount_rate) ** (i + 1))
            
            st.success(f"NPV = Rp {npv:,.2f}")
            
            if npv > 0:
                st.success("✅ Investasi LAYAK (NPV > 0)")
            else:
                st.error("❌ Investasi TIDAK LAYAK (NPV < 0)")
            
            # Hitung IRR (metode iterasi sederhana)
            def calculate_npv(rate, initial, cfs):
                npv = -initial
                for i, cf in enumerate(cfs):
                    npv += cf / ((1 + rate) ** (i + 1))
                return npv
            
            # Cari IRR dengan metode bisection
            low, high = 0.01, 1.0
            for _ in range(100):
                mid = (low + high) / 2
                npv_mid = calculate_npv(mid, initial_investment, cash_flows)
                if abs(npv_mid) < 1:
                    break
                if npv_mid > 0:
                    low = mid
                else:
                    high = mid
            
            irr = mid * 100
            st.success(f"IRR ≈ {irr:.2f}%")
            
            if irr > discount_rate * 100:
                st.success("✅ IRR > Tingkat Diskonto (Layak)")
            else:
                st.error("❌ IRR < Tingkat Diskonto (Tidak Layak)")
    
    with col2:
        st.subheader("Rumus NPV")
        st.latex(r"NPV = -I_0 + \sum_{t=1}^{n} \frac{CF_t}{(1+r)^t}")
        st.markdown("""
        **Keterangan:**
        - I₀ = Investasi awal
        - CFₜ = Cash flow tahun ke-t
        - r = Tingkat diskonto
        - n = Jumlah tahun
        """)
        
        st.subheader("Kriteria Keputusan")
        st.markdown("""
        **NPV:**
        - NPV > 0: Investasi layak
        - NPV = 0: Investasi marginal
        - NPV < 0: Investasi tidak layak
        
        **IRR:**
        - IRR > Tingkat diskonto: Layak
        - IRR < Tingkat diskonto: Tidak layak
        """)

# Fungsi untuk Regresi Linear
def regresi_linear():
    st.header("📈 Regresi Linear")
    st.markdown("Regresi linear digunakan untuk peramalan dan analisis hubungan antar variabel.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Data")
        
        # Option untuk input data
        input_method = st.radio("Metode Input Data:", ["Manual", "Upload CSV"])
        
        if input_method == "Manual":
            n_data = st.number_input("Jumlah Data", value=5, min_value=3, max_value=20)
            
            x_data = []
            y_data = []
            
            for i in range(int(n_data)):
                col_x, col_y = st.columns(2)
                with col_x:
                    x = st.number_input(f"X{i+1}", value=i+1, key=f"x_{i}")
                    x_data.append(x)
                with col_y:
                    y = st.number_input(f"Y{i+1}", value=(i+1)*2, key=f"y_{i}")
                    y_data.append(y)
            
            if st.button("Hitung Regresi"):
                # Hitung regresi linear
                n = len(x_data)
                sum_x = sum(x_data)
                sum_y = sum(y_data)
                sum_xy = sum(x_data[i] * y_data[i] for i in range(n))
                sum_x2 = sum(x * x for x in x_data)
                
                # Koefisien regresi
                b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                a = (sum_y - b * sum_x) / n
                
                # Koefisien korelasi
                sum_y2 = sum(y * y for y in y_data)
                r = (n * sum_xy - sum_x * sum_y) / math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
                
                st.success(f"Persamaan: Y = {a:.2f} + {b:.2f}X")
                st.success(f"Koefisien Korelasi (r) = {r:.4f}")
                st.success(f"Koefisien Determinasi (r²) = {r**2:.4f}")
                
                # Prediksi
                x_pred = st.number_input("Nilai X untuk prediksi:", value=10)
                y_pred = a + b * x_pred
                st.info(f"Prediksi Y = {y_pred:.2f}")
    
    with col2:
        st.subheader("Rumus Regresi Linear")
        st.latex(r"Y = a + bX")
        st.latex(r"b = \frac{n\sum XY - \sum X \sum Y}{n\sum X^2 - (\sum X)^2}")
        st.latex(r"a = \frac{\sum Y - b\sum X}{n}")
        st.latex(r"r = \frac{n\sum XY - \sum X \sum Y}{\sqrt{(n\sum X^2 - (\sum X)^2)(n\sum Y^2 - (\sum Y)^2)}}")
        
        # Grafik regresi (jika data sudah ada)
        if st.button("Tampilkan Grafik Regresi"):
            if 'x_data' in locals() and 'y_data' in locals():
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Scatter plot data
                ax.scatter(x_data, y_data, color='blue', label='Data Aktual')
                
                # Garis regresi
                x_line = np.linspace(min(x_data), max(x_data), 100)
                y_line = a + b * x_line
                ax.plot(x_line, y_line, color='red', label=f'Y = {a:.2f} + {b:.2f}X')
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('Regresi Linear')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)

# Fungsi untuk Optimasi Linear (Metode Grafik)
def optimasi_linear():
    st.header("🎯 Optimasi Linear (Metode Grafik)")
    st.markdown("Menyelesaikan masalah optimasi linear dengan 2 variabel menggunakan metode grafik.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fungsi Objektif")
        obj_type = st.selectbox("Tipe Optimasi:", ["Maksimasi", "Minimasi"])
        c1 = st.number_input("Koefisien X1", value=3)
        c2 = st.number_input("Koefisien X2", value=2)
        
        st.subheader("Constraints (Kendala)")
        st.markdown("Masukkan kendala dalam bentuk: a₁X₁ + a₂X₂ ≤ b")
        
        n_constraints = st.number_input("Jumlah Kendala", value=3, min_value=1, max_value=5)
        
        constraints = []
        for i in range(int(n_constraints)):
            st.markdown(f"**Kendala {i+1}:**")
            col_a1, col_a2, col_b = st.columns(3)
            with col_a1:
                a1 = st.number_input(f"a₁", value=1, key=f"a1_{i}")
            with col_a2:
                a2 = st.number_input(f"a₂", value=1, key=f"a2_{i}")
            with col_b:
                b = st.number_input(f"b", value=10, key=f"b_{i}")
            constraints.append((a1, a2, b))
        
        if st.button("Selesaikan Optimasi"):
            st.success("Solusi akan ditampilkan di grafik →")
    
    with col2:
        st.subheader("Grafik Daerah Feasible")
        
        # Membuat grafik
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Range untuk plotting
        x_range = np.linspace(0, 20, 1000)
        
        # Plot constraints
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for i, (a1, a2, b) in enumerate(constraints):
            if a2 != 0:
                y_constraint = (b - a1 * x_range) / a2
                ax.plot(x_range, y_constraint, color=colors[i % len(colors)], 
                       label=f'{a1}X₁ + {a2}X₂ ≤ {b}')
                ax.fill_between(x_range, 0, y_constraint, alpha=0.1, color=colors[i % len(colors)])
        
        # Plot fungsi objektif (beberapa level)
        for k in [5, 10, 15, 20]:
            if c2 != 0:
                y_obj = (k - c1 * x_range) / c2
                ax.plot(x_range, y_obj, '--', alpha=0.5, color='black')
        
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)
        ax.set_xlabel('X₁')
        ax.set_ylabel('X₂')
        ax.set_title(f'Optimasi Linear: {obj_type} Z = {c1}X₁ + {c2}X₂')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        st.subheader("Metode Penyelesaian")
        st.markdown("""
        1. Gambar semua kendala pada grafik
        2. Tentukan daerah feasible (layak)
        3. Cari titik-titik sudut daerah feasible
        4. Evaluasi fungsi objektif di setiap titik sudut
        5. Pilih titik dengan nilai optimal
        """)

# Main program
if metode == "EOQ (Economic Order Quantity)":
    hitung_eoq()
elif metode == "Break Even Point":
    hitung_bep()
elif metode == "NPV & IRR":
    hitung_npv_irr()
elif metode == "Regresi Linear":
    regresi_linear()
elif metode == "Optimasi Linear":
    optimasi_linear()

# Footer
st.markdown("---")
st.markdown("**Dibuat untuk Tugas Matematika Terapan - Teknik Informatika**")
st.markdown("*Aplikasi ini mendemonstrasikan penerapan metode matematika dalam konteks bisnis dan industri*")
