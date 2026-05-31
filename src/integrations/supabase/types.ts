/**
 * Supabase database types for MedVision AI.
 * Generated to match: supabase/migrations/20260531153000_medvision_scans_persistence.sql
 * Regenerate after schema changes: npx supabase gen types typescript --local > src/integrations/supabase/types.ts
 */

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

/** Matches `ScanFinding` in `@/hooks/useAnalyzeScan` */
export type DbScanFinding = {
  id: string
  title: string
  severity: "critical" | "warning" | "normal"
  confidence: number
  description: string
  location?: string
}

/** Matches `AnalysisResults` in `@/hooks/useAnalyzeScan` (persisted in report_snapshot) */
export type DbAnalysisReportSnapshot = {
  findings: DbScanFinding[]
  overallConfidence: number
  scanType: string
  isValidMedicalScan?: boolean
  modelType?: string
  processingTime?: number
}

export type ScanTypeLabel = "Brain" | "Chest/Lungs" | "Cardiac" | "Bone"

export const SCAN_TYPE_LABELS = [
  "Brain",
  "Chest/Lungs",
  "Cardiac",
  "Bone",
] as const satisfies readonly ScanTypeLabel[]

export type Database = {
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      analysis_results: {
        Row: {
          id: string
          scan_id: string
          findings: DbScanFinding[]
          overall_confidence: number
          scan_type: ScanTypeLabel
          model_type: string | null
          processing_time_ms: number | null
          model_used: string | null
          is_valid_medical_scan: boolean
          hindi_translation: string | null
          report_snapshot: DbAnalysisReportSnapshot
          pdf_storage_path: string | null
          pdf_status: Database["public"]["Enums"]["pdf_export_status"]
          pdf_generated_at: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          scan_id: string
          findings?: DbScanFinding[]
          overall_confidence: number
          scan_type: ScanTypeLabel
          model_type?: string | null
          processing_time_ms?: number | null
          model_used?: string | null
          is_valid_medical_scan?: boolean
          hindi_translation?: string | null
          report_snapshot?: DbAnalysisReportSnapshot
          pdf_storage_path?: string | null
          pdf_status?: Database["public"]["Enums"]["pdf_export_status"]
          pdf_generated_at?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          scan_id?: string
          findings?: DbScanFinding[]
          overall_confidence?: number
          scan_type?: ScanTypeLabel
          model_type?: string | null
          processing_time_ms?: number | null
          model_used?: string | null
          is_valid_medical_scan?: boolean
          hindi_translation?: string | null
          report_snapshot?: DbAnalysisReportSnapshot
          pdf_storage_path?: string | null
          pdf_status?: Database["public"]["Enums"]["pdf_export_status"]
          pdf_generated_at?: string | null
          created_at?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "analysis_results_scan_id_fkey"
            columns: ["scan_id"]
            isOneToOne: true
            referencedRelation: "scans"
            referencedColumns: ["id"]
          },
        ]
      }
      scans: {
        Row: {
          id: string
          user_id: string
          scan_type: ScanTypeLabel
          original_filename: string
          storage_path: string | null
          content_type: string | null
          file_size_bytes: number | null
          status: Database["public"]["Enums"]["scan_status"]
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          scan_type: ScanTypeLabel
          original_filename: string
          storage_path?: string | null
          content_type?: string | null
          file_size_bytes?: number | null
          status?: Database["public"]["Enums"]["scan_status"]
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          scan_type?: ScanTypeLabel
          original_filename?: string
          storage_path?: string | null
          content_type?: string | null
          file_size_bytes?: number | null
          status?: Database["public"]["Enums"]["scan_status"]
          created_at?: string
          updated_at?: string
        }
        Relationships: []
      }
    }
    Views: {
      scan_history: {
        Row: {
          scan_id: string
          user_id: string
          scan_type: ScanTypeLabel
          original_filename: string
          storage_path: string | null
          scan_status: Database["public"]["Enums"]["scan_status"]
          uploaded_at: string
          scan_updated_at: string
          analysis_id: string | null
          overall_confidence: number | null
          model_type: string | null
          processing_time_ms: number | null
          model_used: string | null
          pdf_storage_path: string | null
          pdf_status: Database["public"]["Enums"]["pdf_export_status"] | null
          pdf_generated_at: string | null
          analyzed_at: string | null
        }
        Relationships: []
      }
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      pdf_export_status: "not_requested" | "pending" | "ready" | "failed"
      scan_status: "pending" | "analyzing" | "completed" | "failed"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      pdf_export_status: ["not_requested", "pending", "ready", "failed"] as const,
      scan_status: ["pending", "analyzing", "completed", "failed"] as const,
    },
  },
} as const

export type Scan = Tables<"scans">
export type ScanInsert = TablesInsert<"scans">
export type ScanUpdate = TablesUpdate<"scans">
export type AnalysisResult = Tables<"analysis_results">
export type AnalysisResultInsert = TablesInsert<"analysis_results">
export type AnalysisResultUpdate = TablesUpdate<"analysis_results">
export type ScanHistoryRow = Tables<"scan_history">
export type ScanStatus = Enums<"scan_status">
export type PdfExportStatus = Enums<"pdf_export_status">

export const storagePaths = {
  scanOriginal: (userId: string, scanId: string, filename: string) =>
    `${userId}/${scanId}/${filename}`,
  scanReportPdf: (userId: string, scanId: string) =>
    `${userId}/${scanId}/report.pdf`,
} as const

export const STORAGE_BUCKETS = {
  scans: "medical-scans",
  reports: "medical-reports",
} as const
